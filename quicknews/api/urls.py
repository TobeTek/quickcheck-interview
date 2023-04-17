from django.urls import path
from rest_framework import routers
from api import views

app_name = "api"

urlpatterns = [
    
]

router = routers.DefaultRouter()
router.register(prefix="news", viewset=views.NewsItemListView)

urlpatterns += router.urls
