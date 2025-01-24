from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import *
import json

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        
        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        # Create the message
        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )
        
        # Broadcast to the group
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            event
        )
    
    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user
        }
        html = render_to_string("a_rtchat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)

class PrivateChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        self.other_user = get_object_or_404(User, id=self.other_user_id)
        
        # Create unique room name for the two users
        users = sorted([self.user.id, int(self.other_user_id)])
        self.room_name = f'private_chat_{users[0]}_{users[1]}'
        
        # Join room
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        recipient_id = text_data_json.get('recipient_id')
        
        if recipient_id:
            recipient = get_object_or_404(User, id=recipient_id)
            # Create the message
            message = PrivateMessage.objects.create(
                body=body,
                sender=self.user,
                recipient=recipient
            )
            
            # Broadcast to the private room
            event = {
                'type': 'message_handler',
                'message_id': message.id,
            }
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                event
            )

    def message_handler(self, event):
        message_id = event['message_id']
        message = PrivateMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user
        }
        html = render_to_string("a_rtchat/partials/private_message.html", context=context)
        self.send(text_data=html)