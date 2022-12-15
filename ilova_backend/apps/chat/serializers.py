from rest_framework import serializers
from apps.chat.models import Message, ChatProblem


class ChatProblemSerializer(serializers.ModelSerializer):
    problem = serializers.SerializerMethodField()

    class Meta:
        model = ChatProblem
        fields = ('id', 'problem', 'created_at')
        read_only_fields = ('created_at',)
    
    def get_problem(self, obj):
        return {
            'id': obj.problem.id,
            'title': obj.problem.city + ' ' + obj.problem.district
        }
    
    def create(self, validated_data):
        problem = validated_data.pop('problem')
        chat_problem = ChatProblem.objects.create(**validated_data)
        chat_problem.problem = problem
        chat_problem.save()
        return chat_problem     


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'chat_problem', 'message', 'is_read', 'date')
    
    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message
    
    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance
    