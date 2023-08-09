
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserByToken, CustomUserViewSet

urlpatterns = [
    path('user/by/token/', UserByToken.as_view()),
]
router = DefaultRouter()
router.register("users", CustomUserViewSet)



urlpatterns += router.urls