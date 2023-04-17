from news import views
from django.urls import path

app_name = "news"

urlpatterns = [
    path("search/", views.SearchNewsItemView.as_view(), name="news_search"),
    path("news/", views.NewsItemListView.as_view(), name="news_list"),
    path("news/<int:pk>/", views.NewsItemDetailView.as_view(), name="news_detail"),
    path("stories/", views.StoryListView.as_view(), name="story_list"),
    path("comments/", views.CommentListView.as_view(), name="comment_list"),
    path("jobs/", views.JobListView.as_view(), name="job_list"),
    path("polls/", views.PollListView.as_view(), name="poll_list"),
    path("polloptions/", views.PollOptionsListView.as_view(), name="polloptions_list"),
]
