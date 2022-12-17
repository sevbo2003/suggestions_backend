from rest_framework import serializers
from apps.notification.models import Mahalla


class MahallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahalla
        fields = '__all__'
