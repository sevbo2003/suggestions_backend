from django_filters import rest_framework as filters
from apps.suggestions.models import Problem, ProblemType, Status
from django.db.models import Q


class ProblemFilter(filters.FilterSet):
    district = filters.CharFilter(field_name='district', lookup_expr='icontains')
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Problem
        fields = ['city', 'district', 'problem_types', 'date', 'status']