from rest_framework import serializers
from apps.notification.models import Mahalla, Notification


class MahallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahalla
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    mahalla = MahallaSerializer(many=True)

    class Meta:
        model = Notification
        fields = '__all__'
    
    def create(self, validated_data):
        mahalla_data = validated_data.pop('mahalla')
        notification = Notification.objects.create(**validated_data)
        for mahalla in mahalla_data:
            Mahalla.objects.create(notification=notification, **mahalla)
        return notification
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance
