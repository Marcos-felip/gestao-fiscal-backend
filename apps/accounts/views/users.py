from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.accounts.serializers.users import RegisterSerializer


class RegisterView(CreateAPIView):
    """View para registrar usuários."""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "Usuário registrado com sucesso. Por favor, verifique seu email para confirmar o cadastro."
        }, status=status.HTTP_201_CREATED)
