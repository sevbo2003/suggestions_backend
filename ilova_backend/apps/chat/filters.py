from django_filters import rest_framework as filters
from apps.chat.models import Message


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            'from_problem_user': ['exact'],
            'is_read': ['exact'],
        }
    