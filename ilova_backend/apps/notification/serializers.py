from rest_framework import serializers
from apps.notification.models import Mahalla, Notification
from django.conf import settings

from apps.notification.tasks import send_notification


class MahallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahalla
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    mahalla = MahallaSerializer(many=True)
    image_link = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'image', 'image_link', 'mahalla', 'date']
        read_only_fields = ('image_link',)
    
    def get_image_link(self, obj):
        return settings.SITE_URL + obj.image.url if obj.image else None
        

class NotificationCreateSerializer(serializers.ModelSerializer):
    image_link = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'image', 'image_link', 'mahalla', 'date']
        read_only_fields = ('image_link',)
    
    def get_image_link(self, obj):
        return settings.SITE_URL + obj.image.url if obj.image else None
        
    
    def create(self, validated_data):
        user =  self.context['request'].user
        if user.is_superuser:
            mahalla_data = validated_data.pop('mahalla')
            notification = Notification.objects.create(**validated_data)
            for mahalla in mahalla_data:
                notification.mahalla.add(mahalla)
            send_notification.apply_async(args=['notification',self.context['request'].data])
            return notification
        return serializers.ValidationError("Only admins can perform this operations")
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance