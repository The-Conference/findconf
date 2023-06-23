from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from Conference_crm.permissions.permissions import ReadOnlyOrAdminPermission

from .models import Conference, Favorite
from .serializers import ConferenceSerializer, FavoriteSerialize


class ConferenceList(generics.ListCreateAPIView):
    serializer_class = ConferenceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

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
    permission_classes = [ReadOnlyOrAdminPermission]

    def get_queryset(self):
        return Conference.objects.filter(checked=True)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj



class FavoriteView(APIView):
    bad_request_message = 'An error has occurred'

    def post(self, request, pk):

        conference = Conference.objects.get(pk=pk)
        if not Favorite.objects.filter(user=request.user, conference_id=conference.id).exists():
            Favorite.objects.create(user=request.user, conference=conference)
            return Response({'detail': 'Conference added to favorites'}, status=status.HTTP_200_OK)
        else:
            Favorite.objects.filter(user=request.user, conference=conference).delete()
            return Response({'detail': 'Conference already in favorites'}, status=status.HTTP_200_OK)


    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        if favorites.exists():
            serializer = FavoriteSerialize(favorites, many=True)
            return Response(serializer.data)
        else:
            return Response("No conferences added to favorites yet")

