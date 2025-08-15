from django.urls import path

from apps.news.views.posts import (
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostUpdateAPIView,
    PostSetCardAPIView
)

app_name = 'news'

urlpatterns = [
    path("posts/create/", PostCreateAPIView.as_view(), name="post-create"),
    path("posts/list/", PostListAPIView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostDetailAPIView.as_view(), name="post-detail"),
    path("posts/<int:pk>/update", PostUpdateAPIView.as_view(), name="post-update"),
    path("posts/<int:post_id>/set-card", PostSetCardAPIView.as_view(), name="post-set-card"),
]
