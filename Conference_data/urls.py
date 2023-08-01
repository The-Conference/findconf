from django.urls import path

from .views import ConferenceList, ConferenceDetail


urlpatterns = [
    path('', ConferenceList.as_view()),
    path('<int:pk>/', ConferenceDetail.as_view()),
]
