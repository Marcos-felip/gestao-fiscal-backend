from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from apps.accounts.models import Membership


User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer customizado para retornar dados extras junto com os tokens."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        if getattr(user, 'org_active', None):
            token['org_active'] = user.org_active.slug
            token['org_active_key'] = user.org_active.key if getattr(user.org_active, 'key', None) else None
            try:
                membership = Membership.objects.get(user=user, organization=user.org_active)
                token['role'] = membership.role
            except Membership.DoesNotExist:
                token['role'] = None
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data['email'] = user.email
        data['org_active'] = user.org_active.slug if getattr(user, 'org_active', None) else None
        data['org_active_key'] = user.org_active.key if getattr(user, 'org_active', None) and getattr(user.org_active, 'key', None) else None

        memberships = Membership.objects.filter(
            user=user,
            is_active=True
        ).select_related('organization')
        orgs = []
        for member in memberships:
            orgs.append({
                'slug': member.organization.slug,
                'name': member.organization.name,
                'role': member.role,
                'key': member.organization.key,
            })
        data['org_list'] = orgs

        if getattr(user, 'org_active', None):
            try:
                member = memberships.get(organization=user.org_active)
                data['role'] = member.role
            except Membership.DoesNotExist:
                data['role'] = None
        else:
            data['role'] = None

        return data
