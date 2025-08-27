from rest_framework_simplejwt.views import TokenObtainPairView
from apps.accounts.serializers.auth import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """View que usa o serializer customizado para retornar tokens com dados extras."""

    serializer_class = CustomTokenObtainPairSerializer
