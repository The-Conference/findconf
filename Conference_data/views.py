from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from Conference_crm.permissions.permissions import ReadOnlyOrAdminPermission
from rest_framework.decorators import action
from rest_framework.response import Response

from .managers import ManageFavorite
from .models import Conference, Grant
from .serializers import ConferenceSerializer, ConferenceShortSerializer, GrantSerializer
from .filters import ConferenceFilter, GrantFilter


class GrantViewSet(viewsets.ModelViewSet, ManageFavorite):
    serializer_class = GrantSerializer
    permission_classes = [ReadOnlyOrAdminPermission]
    filterset_class = GrantFilter
    queryset = Grant.objects.filter(checked=True).order_by('reg_date_end')

    def get_queryset(self):
        queryset = self.annotate_qs_is_favorite_field(self.queryset)
        queryset = queryset.prefetch_related('tags')
        return queryset


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name='conf_status', enum=['started', 'starting_soon', 'finished', 'scheduled'],
                             type={'type': 'array', 'minItems': 1, 'maxItems': 4, 'items': {'type': 'string'}},
                             style='form', explode=False),
        ]
    )
)
class ConferenceViewSet(GrantViewSet):
    serializer_class = ConferenceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]
    filterset_class = ConferenceFilter
    queryset = Conference.objects.filter(checked=True).order_by('conf_date_begin')

    @action(methods=['get'], detail=False, serializer_class=ConferenceShortSerializer)
    def calendar(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)
