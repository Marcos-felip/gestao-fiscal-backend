from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.accounts.serializers.users import (
    UserRegisterSerializer,
    OrganizationRegisterSerializer,
    MembershipRegisterSerializer,
)


class UserRegisterView(CreateAPIView):
    """View para registro de usuários."""
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.to_representation(user), status=status.HTTP_201_CREATED)


class OrganizationRegisterView(CreateAPIView):
    """View para registro de organizações."""
    serializer_class = OrganizationRegisterSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        org = serializer.save()
        return Response(serializer.to_representation(org), status=status.HTTP_201_CREATED)


class MembershipRegisterView(CreateAPIView):
    """View para registro de associações."""
    serializer_class = MembershipRegisterSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        membership = serializer.save()
        return Response(serializer.to_representation(membership), status=status.HTTP_201_CREATED)
