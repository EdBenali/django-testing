from django.urls import path

from .views import BlogPostDetailView, BlogPostListView

app_name = "blog"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="post_list"),
    path("<int:pk>/", BlogPostDetailView.as_view(), name="post_detail"),
]
