from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import generics

from Conference_crm.permissions.permissions import ReadOnlyOrAdminPermission
from .models import Conference
from .serializers import ConferenceSerializer
from .filters import ConferenceFilter


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='ordering', enum=['conf_date_begin', '-conf_date_begin']),
            OpenApiParameter(name='conf_status', enum=['started', 'starting_soon', 'finished', 'scheduled'],
                             type={'type': 'array', 'minItems': 1, 'maxItems': 4, 'items': {'type': 'string'}},
                             style='form', explode=False),
        ]
    )
)
class ConferenceList(generics.ListCreateAPIView):
    serializer_class = ConferenceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]
    filterset_class = ConferenceFilter
    queryset = Conference.objects.filter(checked=True)
    ordering_fields = ['conf_date_begin']


class ConferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConferenceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

    def get_queryset(self):
        return Conference.objects.filter(checked=True)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj
