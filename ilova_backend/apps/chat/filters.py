from django_filters import rest_framework as filters
from apps.chat.models import Message


class MessageFilter(filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            'chat_problem': ['exact'],
            'is_read': ['exact'],
        }
    