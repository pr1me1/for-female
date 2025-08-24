from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    GenericAPIView, DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.news.models import Post
from apps.news.serializers.posts import PostCreateSerializer, PostModelSerializer
from apps.text_services.pagination import StandardResultsSetPagination


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context


class PostListAPIView(ListAPIView):
    serializer_class = PostModelSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at", "description")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

    def get_queryset(self):
        return Post.objects.all()


class PostDetailAPIView(RetrieveAPIView):
    serializer_class = PostModelSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        exclude_fields = (
            "created_at",
            "updated_at",
        )
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

    def get_object(self):
        post_id = self.kwargs["pk"]
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404


class PostUpdateAPIView(GenericAPIView):
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        post_id = self.kwargs["pk"]
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author:
            raise PermissionDenied({"error": "Permission Denied"})
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PostSetCardAPIView(GenericAPIView):
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, post_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            post = Post.objects.get(id=post_id)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        card_file = request.FILES.get("card_file")
        if not card_file:
            return Response(
                {
                    "detail": "Card file not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if card_file.size > 5 * 1024 * 1024:
            return Response(
                {
                    "detail": "Card file too big.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if card_file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            return Response(
                {
                    "detail": f"Invalid file format. Allowed formats: {', '.join(['image/jpeg', 'image/png', 'image/gif'])}"
                },
            )

        if post.card and hasattr(post.card, "delete"):
            post.card.delete(save=False)

        post.card = card_file
        post.save(update_fields=["card"])

        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PostDeleteAPIView(DestroyAPIView):
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        post_id = self.kwargs["post_id"]
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        return post

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if request.user != post.author:
            raise PermissionDenied({"error": "Permission Denied"})
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

_all_ = [
    "PostCreateAPIView",
    "PostListAPIView",
    "PostDetailAPIView",
    "PostUpdateAPIView",
    "PostSetCardAPIView",
]
