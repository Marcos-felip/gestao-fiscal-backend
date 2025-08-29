from apps.accounts.models import Membership, Organization
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.text import slugify

User = get_user_model()


class UserRegisterSerializer(serializers.Serializer):
    """Serializer para registrar usuários.

    Recebe full_name, email e password; quebra full_name em first/last.
    Retorna a key do usuário criado.
    """
    full_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Este campo é obrigatório.')
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Já existe um usuário com este email')
        return value.lower()

    def validate(self, attrs):
        pwd = attrs.get('password')
        pwd2 = attrs.get('password_confirm')
        if not pwd or not pwd2:
            raise serializers.ValidationError('As duas senhas devem ser informadas')
        if pwd != pwd2:
            raise serializers.ValidationError('As senhas não coincidem')
        try:
            validate_password(pwd, user=None)
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return attrs

    def create(self, validated_data):
        full_name = validated_data.get('full_name', '').strip()
        password = validated_data.get('password')
        email = validated_data.get('email')
        username = email
        first_name = ''
        last_name = ''
        if full_name:
            parts = full_name.split()
            first_name = parts[0]
            last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        return user

    def to_representation(self, instance):
        return {
            'key': getattr(instance, 'key', None),
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
        }


class OrganizationRegisterSerializer(serializers.Serializer):
    """Serializer para registrar organizações."""

    name = serializers.CharField()
    slug = serializers.SlugField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    organization_type = serializers.ChoiceField(choices=Organization.OrganizationType.choices)

    def validate_slug(self, value):
        if not value:
            raise serializers.ValidationError('Este campo é obrigatório.')
        if Organization.objects.filter(slug__iexact=value).exists():
            raise serializers.ValidationError('Já existe organização com este slug')
        return value

    def create(self, validated_data):
        org = Organization.objects.create(
            name=validated_data['name'],
            slug=validated_data['slug'],
            phone=validated_data.get('phone'),
            organization_type=validated_data['organization_type'],
        )

        return org

    def to_representation(self, instance):
        return {
            'key': getattr(instance, 'key', None),
            'name': instance.name,
            'slug': instance.slug,
            'organization_type': instance.organization_type,
        }


class MembershipRegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de associações.

    Inputs:
      - organization_key (obrigatório)
      - user_key (obrigatório)
      - role (OWNER)
    """

    user_key = serializers.CharField(write_only=True)
    organization_key = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=Membership.Role.choices, write_only=True)

    class Meta:
        model = Membership
        fields = [
            'user_key',
            'organization_key',
            'role'
        ]

    def validate(self, attrs):
        user_obj = None
        user_key = attrs.get('user_key')
        if user_key:
            try:
                user_obj = User.objects.get(key=user_key)
            except User.DoesNotExist:
                raise serializers.ValidationError({'user_key': 'Usuário não encontrado'})

        org_key = attrs.get('organization_key')
        try:
            org_obj = Organization.objects.get(key=org_key)
        except Organization.DoesNotExist:
            raise serializers.ValidationError({'organization_key': 'Organização não encontrada'})

        if Membership.objects.filter(user=user_obj, organization=org_obj).exists():
            raise serializers.ValidationError('Membership já existe para este usuário e organização')

        attrs['user_obj'] = user_obj
        attrs['org_obj'] = org_obj
        return attrs

    def create(self, validated_data):
        user = validated_data['user_obj']
        organization = validated_data['org_obj']
        role = Membership.Role.OWNER
        membership = Membership.objects.create(user=user, organization=organization, role=role)
        if not user.org_active:
            user.org_active = organization
            user.save(update_fields=['org_active'])
        return membership

    def to_representation(self, instance):
        return {
            'user_key': getattr(instance.user, 'key', None),
            'organization_key': getattr(instance.organization, 'key', None),
            'organization_slug': instance.organization.slug,
            'role': instance.role,
        }
