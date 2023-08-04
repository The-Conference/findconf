from django.urls import path

from .views import ConferenceViewSet

urlpatterns = [
    path('', ConferenceViewSet.as_view({'get': 'list'}), name='conf-list'),
    path('favorites/', ConferenceViewSet.as_view({'get': 'favorites'})),
    path('<int:pk>/', ConferenceViewSet.as_view({'get': 'retrieve'}), name='conf-detail'),
    path('<int:pk>/favorite/', ConferenceViewSet.as_view({'get': 'favorite'}))
]
