from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.accounts.views.users import (
    UserRegisterView,
    OrganizationRegisterView,
    MembershipRegisterView,
)
from apps.accounts.views.auth import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/user/', UserRegisterView.as_view(), name='register-user'),
    path('register/organization/', OrganizationRegisterView.as_view(), name='register-organization'),
    path('register/member/', MembershipRegisterView.as_view(), name='register-member'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

