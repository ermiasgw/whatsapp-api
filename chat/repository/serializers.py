from chat.entity.models import ChatRoom,Message, Attachment
from rest_framework import serializers


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'attachment')

class MessageSerializer(serializers.ModelSerializer):
    files = FileAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'content', 'timestamp', 'files')