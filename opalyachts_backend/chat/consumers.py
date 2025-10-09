import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

#we need this to create a message
from .models import ConversationMessage
#

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name=f'chat_{self.room_name}'
        #join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    

    async def disconnect(self):
        
        #leave rooom
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    

    # receive msg from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        conversation_id = data['data']['conversation_id']
        sent_to_id = data['data']['sent_to_id']
        username = data['data']['username']
        body = data['data']['body']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'body':body,
                'name':username
            }
        )

        await self.save_message(conversation_id, body, sent_to_id)





# send msg to web socket
    async def chat_message(self, event):
        username = event['username']
        body = event['body']

        await self.send(text_data=json.dumps({
            'body': body,
            'name':name
        }))

    @sync_to_async
    def save_message(self, conversation_id, body, sent_to_id):
        user = self.scope['user']

        ConversationMessage.objects.create(conversation_id= conversation_id, body=body, sent_to_id=sent_to_id,created_by=user)

