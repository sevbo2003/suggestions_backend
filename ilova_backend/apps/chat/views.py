from rest_framework.viewsets import ModelViewSet, ViewSet
from apps.chat.serializers import MessageSerializer, ChatProblemSerializer, MessageFileSerializer
from apps.chat.models import Message, ChatProblem, MessageFile
from apps.chat.permission import IsOwberOrReadOnly
from apps.suggestions.models import Problem
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ChatViewSet(ModelViewSet):
    queryset = ChatProblem.objects.all()
    serializer_class = ChatProblemSerializer
    permission_classes = [IsOwberOrReadOnly, IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        else:
            return self.queryset.filter(problem__user = self.request.user)
        

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        problem = Problem.objects.get(id=request.data['problem'])
        if request.user.is_authenticated:
            if problem.user == request.user or request.user.is_superuser:
                try:
                    chat_problem = ChatProblem.objects.get(problem=problem)
                    serializer = ChatProblemSerializer(chat_problem)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except:
                    chat_problem = ChatProblem.objects.create(problem=problem)
                    serializer = ChatProblemSerializer(chat_problem)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"message": "You don't have permission to do this operation"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "You don't have permission to do this operation"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.problem.user == request.user or request.user.is_superuser:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def get_read_messages(self, request, pk=None):
        chat = self.get_object()
        page = self.paginate_queryset(Message.objects.filter(chat_problem=chat, is_read=True))
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        queryset = Message.objects.filter(chat_problem=chat, is_read=True)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def get_unread_messages(self, request, pk=None):
        chat = self.get_object()
        page = self.paginate_queryset(Message.objects.filter(chat_problem=chat, is_read=False))
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        queryset = Message.objects.filter(chat_problem=chat, is_read=False)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        chat = self.get_object()
        page = self.paginate_queryset(Message.objects.filter(chat_problem=chat))
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        queryset = Message.objects.filter(chat_problem=chat)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageFileViewSet(ViewSet):
    queryset = MessageFile.objects.all()
    serializer_class = MessageFileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'head', 'options', 'delete']

    def get_object(self):
        return MessageFile.objects.get(id=self.kwargs['pk'])
    
    def perform_destroy(self, instance):
        instance.delete()

    def create(self, request, *args, **kwargs):
        serializer = MessageFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
