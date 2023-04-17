from django_filters import rest_framework as filters
from news.models import NewsItem


class NewsItemFilter(filters.FilterSet):
    min_date = filters.DateTimeFilter(field_name="hn_time_created", lookup_expr="lte")
    max_date = filters.DateTimeFilter(field_name="hn_time_created", lookup_expr="gte")

    min_score = filters.NumberFilter(field_name="price", lookup_expr="lte")
    max_score = filters.NumberFilter(field_name="price", lookup_expr="gte")

    min_descendants = filters.NumberFilter(field_name="price", lookup_expr="lte")
    max_descendants = filters.NumberFilter(field_name="price", lookup_expr="gte")

    class Meta:
        model = NewsItem
        fields = ["deleted", "type", "by", "dead", "parent"]
