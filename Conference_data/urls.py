from django.urls import path

from .views import ConferenceViewSet

urlpatterns = [
    # path('', ConferenceList.as_view()),
    path('', ConferenceViewSet.as_view({'get': 'list'})),
    path('favorites/', ConferenceViewSet.as_view({'get': 'favorites'})),
    path('<int:pk>/', ConferenceViewSet.as_view({'get': 'retrieve'})),
    path('<int:pk>/favorite/', ConferenceViewSet.as_view({'get': 'favorite'}))
]
