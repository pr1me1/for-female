from django.urls import path

from apps.courses.views import (
    CategoryCreateView,
    CategorySetIconView,
    CategoryListView,
    CategoryDetailView,
    CreateCourseAPIView,
    CourseListAPIView,
    CourseSetCardAPIView,
    CourseDetailAPIView
)
from apps.courses.views.webinar import (
    WebinarCreateAPIView,
    WebinarListAPIView
)

app_name = "apps.courses"

urlpatterns = [
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:category_id>/set-icon/', CategorySetIconView.as_view(), name='category-set-icon'),
    path('category/list/', CategoryListView.as_view(), name='category-list'),
    path('category/<int:category_id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('course/create/', CreateCourseAPIView.as_view(), name='course_create'),
    path('course/list/', CourseListAPIView.as_view(), name='course_list'),
    path('course/<int:course_id>/set-card/', CourseSetCardAPIView.as_view(), name='course-set-card'),
    path('course/<int:course_id>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('webinar/create/', WebinarCreateAPIView.as_view(), name='webinar_create'),
    path('webinar/list/', WebinarListAPIView.as_view(), name='webinar_list'),
]
