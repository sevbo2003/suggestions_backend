import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notification'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.close()

    @sync_to_async
    def compare(self, message):
        user = self.scope.get('user', False)
        mahallalar = message['mahalla']
        compare = set(user.mahallalar.all().values_list('id', flat = True)) & set(mahallalar)
        if  len(compare) > 0:
            return True
        return False
    
    async def notification_message(self, event):
        message = event['message']
        if await self.compare(message):
            await self.send(text_data=json.dumps({
                "message": message,
            }))
        