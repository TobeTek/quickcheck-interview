from django_filters import rest_framework as filters
from rest_framework import views, routers, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError

from api.serializers import NewsItemSerializer
from news.models import NewsItem
from api.filters import NewsItemFilter


class NewsItemListView(viewsets.ModelViewSet):
    model = NewsItem
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewsItemFilter
    
    def perform_destroy(self, instance):
        NewsItemSerializer._ensure_is_custom_news(instance)
        return super().perform_destroy(instance)
    
# class NewsItemDetailView(RetrieveUpdateDestroyAPIView):