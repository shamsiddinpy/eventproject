# events/filters.py
import django_filters
from .models import Event


class EventFilter(django_filters.FilterSet):
    """
    Sana oraligʻi va joylashuvi boʻyicha filtrlash imkonini beruvchi Voqealar uchun filtr
    """
    min_date = django_filters.DateTimeFilter(field_name="date", lookup_expr='gte')
    max_date = django_filters.DateTimeFilter(field_name="date", lookup_expr='lte')
    location = django_filters.CharFilter(field_name="location", lookup_expr='icontains')
    created_by = django_filters.NumberFilter(field_name="created_by")

    class Meta:
        model = Event
        fields = ['min_date', 'max_date', 'location', 'created_by']