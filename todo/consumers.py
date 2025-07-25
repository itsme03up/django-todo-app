# WebSocket consumers for the todo app
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TodoConsumer(AsyncWebsocketConsumer):
    """
    Example WebSocket consumer for real-time todo updates.
    This is a basic template - modify according to your needs.
    """
    
    async def connect(self):
        # Join room group
        self.room_group_name = 'todo_updates'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'todo_message',
                'message': message
            }
        )
    
    async def todo_message(self, event):
        # Handle messages from room group
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
