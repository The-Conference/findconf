from rest_framework import generics
from django.shortcuts import get_object_or_404

from .models import Conference
from .serializers import ConferenceSerializer


class ConferenceList(generics.ListCreateAPIView):
    serializer_class = ConferenceSerializer

    def get_queryset(self):
        offline = self.request.query_params.get('offline', None)
        online = self.request.query_params.get('online', None)

        queryset = Conference.objects.filter(checked=True)

        if offline is not None:
            queryset = queryset.filter(offline=bool(offline))

        if online is not None:
            queryset = queryset.filter(online=bool(online))

        return queryset


class ConferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConferenceSerializer

    def get_queryset(self):
        return Conference.objects.filter(checked=True)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj
