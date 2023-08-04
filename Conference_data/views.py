from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import generics

from Conference_crm.permissions.permissions import ReadOnlyOrAdminPermission
from .managers import ManageFavorite
from .models import Conference
from .serializers import ConferenceSerializer
from .filters import ConferenceFilter


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='conf_status', enum=['started', 'starting_soon', 'finished', 'scheduled'],
                             type={'type': 'array', 'minItems': 1, 'maxItems': 4, 'items': {'type': 'string'}},
                             style='form', explode=False),
        ]
    )
)
class ConferenceViewSet(viewsets.ModelViewSet, ManageFavorite):
    queryset = Conference.objects.filter(checked=True)
    serializer_class = ConferenceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]
    filterset_class = ConferenceFilter

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
