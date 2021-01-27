# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from channels.layers import get_channel_layer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("CONNECTED")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.increment_online_count()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'update_users_online',
            }
        )

    def disconnect(self, close_code):
        self.decrement_online_count()
        # Leave room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'update_users_online',
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    def update_users_online(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'online_users': self.get_all_online_users_except_self()
        }))

    def increment_online_count(self):
        user = self.scope['user']
        user.profile.online_count = user.profile.online_count + 1
        user.profile.save()

    def decrement_online_count(self):
        user = self.scope['user']
        if user.profile.online_count > 0:
            user.profile.online_count = user.profile.online_count - 1
            user.profile.save()

    def get_all_online_users_except_self(self):
        user = self.scope['user']
        online_users = User.objects.filter(profile__online_count__gt=0).exclude(id=user.id)
        for user in online_users:
            print(str(user))
        serialized_online_users = [online_user.profile.as_dict() for online_user in online_users]
        return serialized_online_users


class GameInviteConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'invite_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = text_data_json['user']
        if user and user['id'] and isinstance((user['id']), int):

            # Send message to room group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'invite_' + str(user['id']),
                {
                    'type': 'receive_invite',
                    'message': 'Invite to checkers from ' + self.scope['user'].username
                }
            )

    def receive_invite(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))
