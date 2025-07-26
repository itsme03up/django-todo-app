# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.room_group_name = f'chat_task_{self.task_id}'
        self.user = self.scope['user']

        # Join task-specific chat room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        # Send join notification to the room
        username = await self.get_username()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': username,
                'task_id': self.task_id
            }
        )

    async def disconnect(self, close_code):
        # Send leave notification to the room
        username = await self.get_username()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'username': username,
                'task_id': self.task_id
            }
        )
        
        # Leave task-specific chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = await self.get_username()

        user = await self.get_user(username)
        
        # Save message to database
        await self.save_message(user, self.task_id, message)

        # Send message to task-specific chat room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'task_id': self.task_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        task_id = event['task_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message,
            'username': username,
            'task_id': task_id,
            'timestamp': self.get_timestamp()
        }))

    async def user_join(self, event):
        username = event['username']
        task_id = event['task_id']

        # Send join notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'username': username,
            'task_id': task_id,
            'timestamp': self.get_timestamp()
        }))

    async def user_leave(self, event):
        username = event['username']
        task_id = event['task_id']

        # Send leave notification to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'username': username,
            'task_id': task_id,
            'timestamp': self.get_timestamp()
        }))

    @database_sync_to_async
    def get_username(self):
        if hasattr(self.user, 'is_authenticated') and self.user.is_authenticated:
            return self.user.username
        else:
            return f"Guest_{self.channel_name[-8:]}"  # Use last 8 chars of channel name as guest ID

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def save_message(self, user, room, message):
        Message.objects.create(user=user, room=room, content=message)

    def get_timestamp(self):
        import datetime
        return datetime.datetime.now().strftime('%H:%M:%S')
