from .models import Conference
from .serializers import ConferenceSerializer
from rest_framework import generics


class ConferenceList(generics.ListCreateAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


class ConferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
