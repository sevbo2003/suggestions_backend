from rest_framework import serializers
from apps.chat.models import Message, ChatProblem, MessageFile
from apps.suggestions.serializers import ProblemSerializer
from django.conf import settings


class ChatProblemSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()

    class Meta:
        model = ChatProblem
        fields = ('id', 'problem', 'last_message', 'created_at')
        read_only_fields = ('last_message', 'created_at')
    
    def create(self, validated_data):
        problem = validated_data.pop('problem')
        chat_problem = ChatProblem.objects.create(**validated_data)
        chat_problem.problem = problem
        chat_problem.save()
        return chat_problem     


class MessageSerializer(serializers.ModelSerializer):
    file_link = serializers.SerializerMethodField()
    file = serializers.FileField(allow_empty_file = True, use_url = False, write_only=True)

    class Meta:
        model = Message
        fields = ('id', 'chat_problem', 'message','file','file_link', 'sender', 'is_read', 'date')
        read_only_fields = ('date', 'file_link')
    
    def get_file_link(self, obj):
        return settings.SITE_URL + obj.file.url if obj.file else None
    
    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message
    
    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance
    

class MessageFileSerializer(serializers.ModelSerializer):
    file_link = serializers.SerializerMethodField()
    file = serializers.FileField(allow_empty_file = False, use_url = False, write_only=True
    )

    class Meta:
        model = MessageFile
        fields = ('id', 'file', 'file_link')
        read_only_fields = ('file_link',)
    
    def get_file_link(self, obj):
        return settings.SITE_URL + obj.file.url


class MessageIsReadedSerializer(serializers.Serializer):
    messages = serializers.ListField(child=serializers.IntegerField())
