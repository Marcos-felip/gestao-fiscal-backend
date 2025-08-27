from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.accounts.views.users import RegisterView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
]

