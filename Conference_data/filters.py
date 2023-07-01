from django.db.models import Q
from django_filters import rest_framework as filters, BaseInFilter, CharFilter
from django.utils import timezone

from .models import Conference


class CharInFilter(BaseInFilter, CharFilter):
    pass


class ConferenceFilter(filters.FilterSet):
    tags = CharInFilter(field_name='tags__name', lookup_expr='in')
    un_name = CharInFilter(field_name='un_name', lookup_expr='in')
    conf_status = CharInFilter(method='filter_conf_status', lookup_expr='in')

    @staticmethod
    def filter_conf_status(queryset, name, value):
        current_date = timezone.now().date()
        queryset_started = queryset_starting_soon = queryset_finished = \
            queryset_scheduled = queryset_unknown = Conference.objects.none()

        for conf_status in value:
            if conf_status == 'started':
                queryset_started = queryset.filter(
                    Q(conf_date_begin__lte=current_date) &
                    Q(conf_date_end__gte=current_date)
                )
            elif conf_status == 'starting_soon':
                start_date = current_date + timezone.timedelta(days=14)
                queryset_starting_soon = queryset.filter(
                    Q(conf_date_begin__lte=start_date) &
                    Q(conf_date_begin__gt=current_date)
                )
            elif conf_status == 'finished':
                queryset_finished = queryset.filter(
                    Q(conf_date_end__lt=current_date) |
                    (Q(conf_date_end__isnull=True) & Q(conf_date_begin__lt=current_date))
                )
            elif conf_status == 'scheduled':
                queryset_scheduled = queryset.filter(conf_date_begin__gt=current_date)
            elif conf_status == 'unknown':
                queryset_unknown = queryset.filter(
                    Q(conf_date_begin__isnull=True) |
                    Q(conf_date_end__isnull=True)
                )
        return queryset_started | queryset_starting_soon | queryset_finished | queryset_scheduled | queryset_unknown

    class Meta:
        model = Conference
        fields = ['offline', 'online', 'rinc', 'vak', 'wos', 'scopus', 'tags', 'un_name', 'conf_status']
