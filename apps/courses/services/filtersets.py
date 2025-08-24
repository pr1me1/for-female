from django_filters import rest_framework as filters

from apps.courses.models import Category, Course, Webinar


class CourseFilterByCategory(filters.FilterSet):
    category = filters.ModelChoiceFilter(queryset=Category.objects.all())
    category__name = filters.CharFilter(
        field_name="category__name", lookup_expr="iexact"
    )

    class Meta:
        model = Course
        fields = ["category", "category__name"]


class WebinarFilterByCategory(filters.FilterSet):
    category = filters.ModelChoiceFilter(queryset=Category.objects.all())
    category__name = filters.CharFilter(
        field_name="category__name", lookup_expr="iexact"
    )

    class Meta:
        model = Webinar
        fields = ["category", "category__name"]
