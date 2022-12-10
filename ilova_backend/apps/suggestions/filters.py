from django_filters import rest_framework as filters
from apps.suggestions.models import Problem, ProblemType, Status
from datetime import timedelta, date

class ProblemFilter(filters.FilterSet):
    district = filters.CharFilter(field_name='district', lookup_expr='icontains')
    date_choices = (
        ('today', 'Today'),
        ('yesterday', 'Yesterday'),
        ('this_week', 'This Week'),
        ('last_week', 'Last Week'),
        ('this_month', 'This Month'),
        ('last_month', 'Last Month'),
        ('this_year', 'This Year'),
        ('last_year', 'Last Year'),
    )
    date = filters.ChoiceFilter(choices=date_choices, method='filter_date')
    status_choices = (
        ('solved', 'Solved'),
        ('pending', 'Pending'),
        ('fake', 'Fake'),
    )
    status = filters.ChoiceFilter(choices=Status.choices)

    class Meta:
        model = Problem
        fields = ['city', 'district', 'problem_types', 'date', 'status']
    
    def filter_date(self, queryset, name, value):
        today = date.today()
        if value == 'today':
            return queryset.filter(date__date=today)
        elif value == 'yesterday':
            return queryset.filter(date__date=today - timedelta(days=1))
        elif value == 'this_week':
            return queryset.filter(date__week=today.isocalendar()[1])
        elif value == 'last_week':
            return queryset.filter(date__week=today.isocalendar()[1] - 1)
        elif value == 'this_month':
            return queryset.filter(date__month=today.month)
        elif value == 'last_month':
            return queryset.filter(date__month=today.month - 1)
        elif value == 'this_year':
            return queryset.filter(date__year=today.year)
        elif value == 'last_year':
            return queryset.filter(date__year=today.year - 1)