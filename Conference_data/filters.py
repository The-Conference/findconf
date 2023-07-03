from django.db.models import Q
from django_filters import rest_framework as filters, BaseInFilter, CharFilter
from django.utils import timezone

from .models import Conference


class CharInFilter(BaseInFilter, CharFilter):
    pass


class ConferenceFilter(filters.FilterSet):
    tags = CharInFilter(field_name='tags__name', lookup_expr='in', distinct=True)
    un_name = CharInFilter(field_name='un_name', lookup_expr='in', distinct=True)
    conf_status = CharInFilter(method='filter_conf_status', lookup_expr='in', distinct=True)

    @staticmethod
    def filter_conf_status(queryset, name, value):
        current_date = timezone.now().date()
        qs_started = qs_starting_soon = qs_finished = qs_scheduled = Conference.objects.none()

        for conf_status in value:
            if conf_status == 'started':
                qs_started = queryset.filter(
                    Q(conf_date_begin__lte=current_date) &
                    Q(conf_date_end__gte=current_date)
                )
            elif conf_status == 'starting_soon':
                start_date = current_date + timezone.timedelta(days=14)
                qs_starting_soon = queryset.filter(
                    Q(conf_date_begin__lte=start_date) &
                    Q(conf_date_begin__gt=current_date)
                )
            elif conf_status == 'finished':
                qs_finished = queryset.filter(
                    Q(conf_date_end__lt=current_date) |
                    (Q(conf_date_end__isnull=True) & Q(conf_date_begin__lt=current_date))
                )
            elif conf_status == 'scheduled':
                qs_scheduled = queryset.filter(conf_date_begin__gt=current_date)
            else:
                return qs_started
        return qs_started | qs_starting_soon | qs_finished | qs_scheduled

    class Meta:
        model = Conference
        fields = ['offline', 'online', 'rinc', 'vak', 'wos', 'scopus', 'tags', 'un_name', 'conf_status']
