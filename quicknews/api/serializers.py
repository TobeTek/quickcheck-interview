from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from news.models import NewsItem


class NewsItemSerializer(serializers.ModelSerializer):
    parent = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:newsitem-detail'
    )
    
    class Meta:
        model = NewsItem
        fields = (
            "id",
            "hn_id",
            "deleted",
            "type",
            "by",
            "hn_time_created",
            "pulled_at",
            "dead",
            "parent",
            "text",
            "url",
            "title",
            "descendants",
            "score",
            "parent_poll",
        )

        extra_kwargs = {
            'hn_id': {'read_only': True},
            'hn_time_created': {'read_only': True}
        }
    
    @staticmethod
    def _ensure_is_custom_news(news_item: NewsItem):
        if news_item.hn_id:
            raise ValidationError("Can not delete/edit news pulled from HackerNews")
        
    def update(self, instance, validated_data):
        self._ensure_is_custom_news(instance)
        return super().update(instance, validated_data)
    