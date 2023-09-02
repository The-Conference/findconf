import re

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.utils import timezone
from django_filters import rest_framework, BaseInFilter, CharFilter, OrderingFilter, DateFromToRangeFilter

from .models import Conference, Grant


class CharInFilter(BaseInFilter, CharFilter):
    pass


class CustomOrderingFilter(OrderingFilter):
    """Hides field name used for ordering and replaces it with custom keywords."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('date_asc', 'Date'),
            ('date_desc', 'Date (descending)'),
        ]

    def filter(self, qs, value):
        if value:
            if 'date_asc' in value:
                return qs.order_by('conf_date_begin')
            else:
                return qs.order_by('-conf_date_begin')
        return super().filter(qs, value)


class ConferenceFilter(rest_framework.FilterSet):
    tags = CharInFilter(field_name='tags__name', lookup_expr='in', distinct=True)
    un_name = CharInFilter(field_name='un_name', lookup_expr='in', distinct=True)
    conf_status = CharInFilter(method='filter_conf_status', lookup_expr='in', distinct=True)
    conf_date_begin = DateFromToRangeFilter()
    conf_date_end = DateFromToRangeFilter()
    search = CharFilter(method='text_search', distinct=True)
    ordering = CustomOrderingFilter()

    @staticmethod
    def text_search(queryset, name, value):
        """Search uses Postgres dialect, will not work with SQLite."""
        search_vector = (
                SearchVector('title', 'synopsis', 'description', weight='A', config='russian') +
                SearchVector('un_name', 'conf_address', weight='B', config='russian')
        )
        search_string = re.sub(r'\s+', ' | ', value)
        search_query = SearchQuery(search_string, config='russian', search_type='raw')
        return queryset.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')

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
        fields = ['offline', 'online', 'rinc', 'vak', 'wos', 'scopus', 'tags', 'un_name', 'conf_status',
                  'conf_date_begin', 'conf_date_end']


class GrantFilter(rest_framework.FilterSet):
    tags = CharInFilter(field_name='tags__name', lookup_expr='in', distinct=True)
    un_name = CharInFilter(field_name='un_name', lookup_expr='in', distinct=True)

    class Meta:
        model = Grant
        fields = ['un_name']
