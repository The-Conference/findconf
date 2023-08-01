from django.contrib.auth import get_user_model
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserByToken, CustomUserViewSet

urlpatterns = [
    path('by/token/', UserByToken.as_view()),
]
router = DefaultRouter()
router.register("users", CustomUserViewSet)

User = get_user_model()

urlpatterns += router.urls