from django.urls import path

from .views import ConferenceList, ConferenceDetail, FavoriteView

urlpatterns = [
    path('', ConferenceList.as_view()),
    path('<int:pk>/', ConferenceDetail.as_view()),
    path('favorite/<int:pk>/', FavoriteView.as_view()),
    path('favorite/', FavoriteView.as_view())
]
