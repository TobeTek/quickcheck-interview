from django.contrib import admin
from django.contrib.admin import ModelAdmin
from news.models import NewsItem

# Register your models here.
@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    ordering = ["pulled_at"]
    list_display = [
        "id",
        "hn_id",
        "title",
        "type_label",
        "descendants",
        "score",
        "parent",
    ]
    search_fields = ["id", "hn_id", "text", "title", "by"]
