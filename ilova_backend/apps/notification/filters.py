from django_filters import rest_framework as filters
from apps.notification.models import Mahalla


class MahallaFilter(filters.FilterSet):
    
    class Meta:
        model = Mahalla
        fields = {
            'district': ['icontains'],
            'mahalla': ['icontains'],
        }