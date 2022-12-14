import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.problem_id = self.scope['url_route']['kwargs']['problem_id']
        user = self.scope.get('user', False)
        print(user.id)
        self.problem_id_name = 'problem_%s' % self.problem_id
        await self.channel_layer.group_add(
            self.problem_id_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.problem_id_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope.get('user', False)
        is_read = False
        problem_id = self.problem_id
        if user.is_authenticated:
            await self.save_message(message, user)
            await self.channel_layer.group_send(
                self.problem_id_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user.username,
                    'is_read': is_read,
                    'problem_id': problem_id
                }
            )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        is_read = event['is_read']
        problem_id = event['problem_id']
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'is_read': is_read,
            'problem_id': problem_id
        }))
    
    @sync_to_async
    def save_message(self, message, problem_id):
        Message.objects.create(
            message=message,
            from_problem_user=problem_id
        )
