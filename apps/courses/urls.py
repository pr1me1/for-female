from django.urls import path

from apps.courses.views import (
    CategoryCreateView,
    CategorySetIconView,
    CategoryListView,
    CategoryDetailView,
    CreateCourseAPIView,
    CourseListAPIView,
    CourseSetCardAPIView,
    CourseDetailAPIView,
)
from apps.courses.views.lesson import (
    LessonCreateAPIView,
    LessonListAPIView,
    LessonDetailAPIView,
    LessonUpdateAPIView,
    LessonDeleteAPIView,
)
from apps.courses.views.module import (
    CreateModuleAPIView,
    ModuleListAPIView,
    ModuleDetailAPIView,
    ModuleUpdateAPIView,
    ModuleDeleteAPIView,
)
from apps.courses.views.webinar import (
    WebinarCreateAPIView,
    WebinarListAPIView,
    WebinarSetCardAPIView,
    WebinarDetailAPIView,
)

app_name = "apps.courses"

urlpatterns = [
    path("category/create/", CategoryCreateView.as_view(), name="category_create"),
    path(
        "category/<int:category_id>/set-icon/",
        CategorySetIconView.as_view(),
        name="category-set-icon",
    ),
    path("category/list/", CategoryListView.as_view(), name="category-list"),
    path(
        "category/<int:category_id>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path("course/create/", CreateCourseAPIView.as_view(), name="course_create"),
    path("course/list/", CourseListAPIView.as_view(), name="course_list"),
    path(
        "course/<int:course_id>/set-card/",
        CourseSetCardAPIView.as_view(),
        name="course-set-card",
    ),
    path(
        "course/<int:course_id>/", CourseDetailAPIView.as_view(), name="course-detail"
    ),
    path("webinar/create/", WebinarCreateAPIView.as_view(), name="webinar_create"),
    path("webinar/list/", WebinarListAPIView.as_view(), name="webinar_list"),
    path(
        "webinar/<int:webinar_id>/set-card/",
        WebinarSetCardAPIView.as_view(),
        name="set-card",
    ),
    path(
        "webinar/<int:webinar_id>/",
        WebinarDetailAPIView.as_view(),
        name="webinar_detail",
    ),
    path(
        "course/<int:course_id>/module/create/",
        CreateModuleAPIView.as_view(),
        name="module-create",
    ),
    path(
        "course/<int:course_id>/module/list/",
        ModuleListAPIView.as_view(),
        name="module-list",
    ),
    path(
        "module/<int:module_id>/", ModuleDetailAPIView.as_view(), name="module-detail"
    ),
    path(
        "module/<int:module_id>/update/",
        ModuleUpdateAPIView.as_view(),
        name="module-update",
    ),
    path(
        "module/<int:module_id>/delete/",
        ModuleDeleteAPIView.as_view(),
        name="module-delete",
    ),
    path(
        "module/<int:module_id>/lesson/create/",
        LessonCreateAPIView.as_view(),
        name="lesson-create",
    ),
    path(
        "module/<int:module_id>/lesson/list/",
        LessonListAPIView.as_view(),
        name="lesson-list",
    ),
    path(
        "lesson/<int:lesson_id>/", LessonDetailAPIView.as_view(), name="lesson-detail"
    ),
    path(
        "lesson/<int:lesson_id>/update",
        LessonUpdateAPIView.as_view(),
        name="lesson-update",
    ),
    path(
        "lesson/<int:lesson_id>/delete",
        LessonDeleteAPIView.as_view(),
        name="lesson-delete",
    ),
]
