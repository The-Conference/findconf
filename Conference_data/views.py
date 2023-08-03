from django.db.models import OuterRef, Exists
from rest_framework import generics, status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Conference_crm.permissions.permissions import ReadOnlyOrAdminPermission

from .models import Conference, Favorite
from .serializers import ConferenceSerializer
from django.contrib.contenttypes.models import ContentType


class ManageFavorite:
    @action(
        detail=True,
        methods=['get'],
        url_path='favorite',
        permission_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, pk):
        instance = self.get_object()
        content_type = ContentType.objects.get_for_model(instance)
        favorite_obj, created = Favorite.objects.get_or_create(
            user=request.user, content_type=content_type, object_id=instance.id
        )

        if created:
            return Response(
                {'message': 'Контент добавлен в избранное'},
                status=status.HTTP_201_CREATED
            )
        else:
            favorite_obj.delete()
            return Response(
                {'message': 'Контент удален из избранного'},
                status=status.HTTP_200_OK
            )

    def annotate_qs_is_favorite_field(self, queryset):
        if self.request.user.is_authenticated:
            is_favorite_subquery = Favorite.objects.filter(
                object_id=OuterRef('pk'),
                user=self.request.user,
                content_type=ContentType.objects.get_for_model(queryset.model)
            )
            queryset = queryset.annotate(is_favorite=Exists(is_favorite_subquery))
        return queryset

    @action(
        detail=False,
        methods=['get'],
        url_path='favorites',
        permission_classes=[IsAuthenticated, ]
    )
    def favorites(self, request):
        queryset = self.get_queryset().filter(is_favorite=True)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class ConferenceList(generics.ListCreateAPIView):
#     serializer_class = ConferenceSerializer
#     permission_classes = [ReadOnlyOrAdminPermission]
#
#     def get_queryset(self):
#         offline = self.request.query_params.get('offline', None)
#         online = self.request.query_params.get('online', None)
#
#         queryset = Conference.objects.filter(checked=True)
#
#         if offline is not None:
#             queryset = queryset.filter(offline=bool(offline))
#
#         if online is not None:
#             queryset = queryset.filter(online=bool(online))
#
#         return queryset


# class ConferenceDetail(generics.RetrieveUpdateDestroyAPIView, ):
#     serializer_class = ConferenceSerializer
#     permission_classes = [ReadOnlyOrAdminPermission]
#
#     def get_queryset(self):
#         return Conference.objects.filter(checked=True)
#
#     def get_object(self):
#         queryset = self.get_queryset()
#         obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
#         return obj

class ConferenceViewSet(viewsets.ModelViewSet, ManageFavorite):
    queryset = Conference.objects.filter(checked=True)
    serializer_class = ConferenceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

    def get_object(self, queryset=None, **kwargs):
        queryset = queryset or self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

    def get_queryset(self):
        offline = self.request.query_params.get('offline', None)
        online = self.request.query_params.get('online', None)

        queryset = Conference.objects.filter(checked=True)

        if offline is not None:
            queryset = queryset.filter(offline=bool(offline))

        if online is not None:
            queryset = queryset.filter(online=bool(online))
        queryset = self.annotate_qs_is_favorite_field(queryset)
        return queryset
