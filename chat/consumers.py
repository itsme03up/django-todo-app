# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.room_group_name = f'chat_task_{self.task_id}'

        # Join task-specific chat room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave task-specific chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to task-specific chat room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'task_id': self.task_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        task_id = event['task_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'task_id': task_id
        }))
