from django_filters import rest_framework as filters

from apps.courses.models import Category, Course


class CategoryFilter(filters.FilterSet):
    category = filters.ModelChoiceFilter(queryset=Category.objects.all())
    category__name = filters.CharFilter(field_name='category__name', lookup_expr='iexact')

    class Meta:
        model = Course
        fields = ['category', 'category__name']
