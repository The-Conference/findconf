from rest_framework import viewsets
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from Conference_crm.permissions.permissions import ReadOnlyOrAdminPermission
from .managers import ManageFavorite
from .models import Conference
from .serializers import ConferenceSerializer
from .filters import ConferenceFilter


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name='conf_status', enum=['started', 'starting_soon', 'finished', 'scheduled'],
                             type={'type': 'array', 'minItems': 1, 'maxItems': 4, 'items': {'type': 'string'}},
                             style='form', explode=False),
        ]
    )
)
class ConferenceViewSet(viewsets.ModelViewSet, ManageFavorite):
    serializer_class = ConferenceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]
    filterset_class = ConferenceFilter

    def get_queryset(self):
        queryset = Conference.objects.filter(checked=True).order_by('conf_date_begin')
        queryset = self.annotate_qs_is_favorite_field(queryset)
        return queryset
