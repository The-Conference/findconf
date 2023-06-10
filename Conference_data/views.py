from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone

from rest_framework import generics
from Conference_crm.permissions.permissions import ReadOnlyOrAdminPermission

from .models import Conference
from .serializers import ConferenceSerializer


class ConferenceList(generics.ListCreateAPIView):
    serializer_class = ConferenceSerializer
    permission_classes = [ReadOnlyOrAdminPermission]

    def get_queryset(self):
        offline = self.request.query_params.getlist('offline')
        online = self.request.query_params.getlist('online')
        rinc = self.request.query_params.getlist('rinc')
        vak = self.request.query_params.getlist('vak')
        wos = self.request.query_params.getlist('wos')
        scopus = self.request.query_params.getlist('scopus')
        tags = self.request.query_params.getlist('tags')
        conf_status = self.request.query_params.get('conf_status')
        un_name = self.request.query_params.get('un_name')

        boolean_mapping = {'true': True, 'false': False}
        conf_status_mapping = {
            'started': 'Конференция началась',
            'starting_soon': 'Конференция скоро начнётся',
            'finished': 'Конференция окончена',
            'unknown': 'Неизвестно (уточнить у организатора)',
        }

        queryset = Conference.objects.filter(checked=True)

        if offline:
            offline_values = [boolean_mapping.get(value.lower()) for value in offline]
            queryset = queryset.filter(offline__in=offline_values)

        if online:
            online_values = [boolean_mapping.get(value.lower()) for value in online]
            queryset = queryset.filter(online__in=online_values)

        if rinc:
            rinc_values = [boolean_mapping.get(value.lower()) for value in rinc]
            queryset = queryset.filter(rinc__in=rinc_values)

        if vak:
            vak_values = [boolean_mapping.get(value.lower()) for value in vak]
            queryset = queryset.filter(vak__in=vak_values)

        if wos:
            wos_values = [boolean_mapping.get(value.lower()) for value in wos]
            queryset = queryset.filter(wos__in=wos_values)

        if scopus:
            scopus_values = [boolean_mapping.get(value.lower()) for value in scopus]
            queryset = queryset.filter(scopus__in=scopus_values)

        if tags:
            queryset = queryset.filter(tags__name__in=tags)

        if un_name:
            queryset = queryset.filter(un_name__icontains=un_name)

        if conf_status:
            mapped_conf_status = conf_status_mapping.get(conf_status)
            if mapped_conf_status:
                current_date = timezone.now().date()
                if mapped_conf_status == 'Конференция началась':
                    queryset = queryset.filter(
                        Q(conf_date_begin__lte=current_date) &
                        Q(conf_date_end__gte=current_date)
                    )
                elif mapped_conf_status == 'Конференция скоро начнётся':
                    start_date = current_date + timedelta(days=2)
                    queryset = queryset.filter(conf_date_begin=start_date)
                elif mapped_conf_status == 'Конференция окончена':
                    queryset = queryset.filter(conf_date_end__lt=current_date)
                elif mapped_conf_status == 'Неизвестно (уточнить у организатора)':
                    queryset = queryset.filter(
                        Q(conf_date_begin__isnull=True) |
                        Q(conf_date_end__isnull=True)
                    )

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
