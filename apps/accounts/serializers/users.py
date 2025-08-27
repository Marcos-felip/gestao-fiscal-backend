from apps.accounts.models import Membership, Organization
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.text import slugify


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registrar usuários."""

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    organization_slug = serializers.SlugField(write_only=True, required=True)
    organization_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            'password_confirm',
            'organization_name',
            'organization_slug',
        ]

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("O email deve ser informado")
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Já existe um usuário com este email")
        return value.lower()

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if not password or not password_confirm:
            raise serializers.ValidationError("As duas senhas devem ser informadas")
        if password != password_confirm:
            raise serializers.ValidationError("As senhas não coincidem")

        ## usa validadores configurados em AUTH_PASSWORD_VALIDATORS
        try:
            validate_password(password, user=None)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        org_slug = slugify(attrs.get('organization_slug'))
        if Organization.objects.filter(slug__iexact=org_slug).exists():
            raise serializers.ValidationError({"organization_slug": "Já existe uma organização com este slug"})
        attrs['organization_slug'] = org_slug
        
        if not attrs.get('organization_name'):
            raise serializers.ValidationError({"organization_name": "O nome da organização é obrigatório"})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        org_name = validated_data.pop('organization_name', None)
        org_slug = validated_data.pop('organization_slug', None)

        ## cria usuário
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = email
        user = User.objects.create_user(username=username, email=email, password=password, **validated_data)

        ## cria organização e membership
        if org_name and org_slug:
            org = Organization.objects.create(
                name=org_name,
                slug=org_slug
            )
            Membership.objects.create(
                user=user,
                organization=org,
                role=Membership.Role.OWNER,
            )
            user.org_active = org
            user.save()

        return user