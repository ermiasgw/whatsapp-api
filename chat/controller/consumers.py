import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from chat.entity.models import ChatRoom, Message
from chat.repository.serializers import MessageSerializer
from django.core.files.base import ContentFile

class ChatConsumer(WebsocketConsumer):
 
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.user = None
        self.ChatRoom = None
 
    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return
     
        self.accept()
        self.room_name = f"{self.scope['url_route']['kwargs']['room_name']}"
        self.ChatRoom, created = ChatRoom.objects.get_or_create(name=self.room_name)
        self.ChatRoom.join(self.scope["user"])
    
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name,
        )
        messages = self.ChatRoom.messages.all().order_by("-timestamp")[0:50]
        self.send(text_data=json.dumps(MessageSerializer(messages, many=True).data))
        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )
 
    def receive(self, text_data):
        data = json.loads(text_data)
        text_message = data.get('text_message', '')
        files_data = data.get('files', [])
        message = Message.objects.create(sender=self.scope['user'], content=text_message, chat_room=self.ChatRoom )
        for file_data in files_data:
            self.save_file(message, file_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "chat.message", "message": message}
        )
        
    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(MessageSerializer(message).data))
        

    def save_file(self, message, file_data):
        binary_data = file_data['content'].encode('utf-8')  
        file_name = file_data['name']
        file_content = ContentFile(binary_data, name=file_name)
        message.files.create(attachment=file_content)
        

        
            