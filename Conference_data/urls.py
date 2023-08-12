from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework.generics import ListAPIView

from .views import ConferenceViewSet
from .models import Tag, Conference
from .serializers import TagSerializer, UniversitySerializer

router = DefaultRouter()
router.register('', ConferenceViewSet, basename="api")

urlpatterns = [
    path('lists/tags/',
         ListAPIView.as_view(queryset=Tag.objects.all(),
                             serializer_class=TagSerializer,
                             pagination_class=None),
         name='tag-list'),
    path('lists/universities/',
         ListAPIView.as_view(queryset=Conference.objects.values('un_name').distinct(),
                             serializer_class=UniversitySerializer,
                             pagination_class=None),
         name='un-list'),
]

urlpatterns += router.urls
