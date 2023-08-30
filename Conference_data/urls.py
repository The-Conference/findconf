from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework.generics import ListAPIView

from .views import ConferenceViewSet, GrantViewSet
from .models import Tag, Conference
from .serializers import TagSerializer, UniversitySerializer

router = DefaultRouter()
router.register('confs', ConferenceViewSet)
router.register('grants', GrantViewSet)

urlpatterns = [
    path('lists/tags/',
         ListAPIView.as_view(queryset=Tag.objects.all(),
                             serializer_class=TagSerializer,
                             pagination_class=None),
         name='tag-list'),
    path('lists/universities/',
         ListAPIView.as_view(queryset=Conference.objects.filter(checked=True).values('un_name').distinct(),
                             serializer_class=UniversitySerializer,
                             pagination_class=None),
         name='un-list'),
]

urlpatterns += router.urls
