from rest_framework import serializers
from apps.chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'from_problem_user', 'message', 'is_read', 'date')
    
    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message
    
    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance
    