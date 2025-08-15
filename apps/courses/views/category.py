from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.courses.models import Category
from apps.courses.serializers.category import CategoryCreateSerializer, CategoryModelSerializer
from apps.text_services.pagination import StandardResultsSetPagination


class CategoryCreateView(GenericAPIView):
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = serializer.create(serializer.validated_data)

        return Response(CategoryModelSerializer(response).data, status=status.HTTP_201_CREATED)


class CategorySetIconView(GenericAPIView):
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticated]

    # authentication_classes = [JWTAuthentication]

    def patch(self, request, category_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"detail": "Category with this id does not exist."}, status=status.HTTP_404_NOT_FOUND)

        category_icon = request.FILES.get('category_icon')
        if not category_icon:
            return Response({"detail": "Icon file doesnt provided"}, status=status.HTTP_404_NOT_FOUND)

        if category_icon.size > 1024 * 1024:
            return Response({"detail": "Icon file too big"}, status=status.HTTP_400_BAD_REQUEST)

        allowed_formats = ['image/jpeg', 'image/png', 'image/gif']

        if category_icon.content_type not in allowed_formats:
            return Response({"detail": f"Invalid file format. Allowed formats: {', '.join(allowed_formats)}"}, )

        if category.icon and hasattr(category.icon, 'delete'):
            category.icon.delete(save=False)

        category.icon = category_icon
        category.save()
        return Response(CategoryModelSerializer(category).data, status=status.HTTP_200_OK)


class CategoryListView(ListAPIView):
    serializer_class = CategoryModelSerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    pagination_class = StandardResultsSetPagination


class CategoryDetailView(GenericAPIView):
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAdminUser]

    def _get_object(self, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Exception as e:
            return Response({"detail": "Category with this id does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return category

    def get(self, request, category_id, *args, **kwargs):
        category = self._get_object(category_id)
        return Response(self.serializer_class(category).data, status=status.HTTP_200_OK)

    def delete(self, request, category_id, *args, **kwargs):
        category = self._get_object(category_id)
        category.delete()

        return Response({"detail": "Category has been deleted."}, status=status.HTTP_200_OK)

    def patch(self, request, category_id, *args, **kwargs):
        category = self._get_object(category_id)
        serializer = self.serializer_class(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


_all_ = ['CategoryCreateView', 'CategorySetIconView', 'CategoryListView', 'CategoryDetailView']
