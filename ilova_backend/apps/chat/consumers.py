import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from apps.chat.models import Message, ChatProblem, SenderType
from apps.chat.serializers import MessageSerializer
from apps.suggestions.models import Problem


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        user = self.scope.get('user', False)
        chat = await self.get_chat(self.chat_id)
        chat_user = await self.get_chat_user(chat.problem_id)
        if not user.is_authenticated or not chat:
            await self.close()
        if chat_user != user:
            if not user.is_staff:
                await self.close()
        self.chat_id_name = 'chat_%s' % self.chat_id
        await self.channel_layer.group_add(
            self.chat_id_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_id_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        file = text_data_json['file'] if 'file' in text_data_json else None
        user = self.scope.get('user', False)
        is_read = False
        chat_id = self.chat_id
        if user.is_staff:
            sender = 'admin'
        else:
            sender = 'user'
        if user.is_authenticated:
            reuturn_message = await self.main_message_owerride_func(message, chat_id, sender, file)
            await self.channel_layer.group_send(
                self.chat_id_name,
                {
                    'type': 'chat_message',
                    'message': reuturn_message,
                }
            )
        
    def main_message_owerride_func(self, message, chat_id, sender, file):
        if file:
            return self.save_media_message(message, chat_id, sender, file)
        return self.save_message(message, chat_id, sender, file)

    @sync_to_async
    def get_chat(self, chat_id):
        try:
            chat = ChatProblem.objects.get(id=chat_id)
        except ChatProblem.DoesNotExist:
            chat = None
        return chat
    
    @sync_to_async
    def get_chat_user(self, problem_id):
        try:
            chat = Problem.objects.get(id=problem_id)
            return chat.user
        except ChatProblem.DoesNotExist:
            chat = None
        return chat

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    # @sync_to_async
    # def send_media_message(self, message, chat_id, sender, file):
    #     try:
    #         chat = ChatProblem.objects.get(id=chat_id)
    #     except ChatProblem.DoesNotExist:
    #         chat = ChatProblem.objects.create(problem_id=chat_id)
    #     Message.objects.create(
    #         message=message,
    #         chat_problem=chat,
    #         sender=SenderType[sender.upper()],
    #         file=file
    #     )

    @sync_to_async
    def save_message(self, message, chat_id, sender, file):
        try:
            chat = ChatProblem.objects.get(id=chat_id)
        except ChatProblem.DoesNotExist:
            chat = ChatProblem.objects.create(problem_id=chat_id)
        message = Message.objects.create(
            message=message,
            chat_problem=chat,
            sender=SenderType[sender.upper()],
        )
        return MessageSerializer(message).data
    
    @sync_to_async
    def save_media_message(self, message, chat_id, sender, file):
        try:
            chat = ChatProblem.objects.get(id=chat_id)
        except ChatProblem.DoesNotExist:
            chat = ChatProblem.objects.create(problem_id=chat_id)
        message = Message.objects.create(
            message=message,
            chat_problem=chat,
            sender=SenderType[sender.upper()],
            file=file
        )
        return MessageSerializer(message).data
