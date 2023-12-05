from django.db import models
from django.contrib.auth import get_user_model
import os

user = get_user_model()


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(user, blank=True)
    max_members = models.IntegerField(null=True)

    def get_members_count(self):
        return self.members.count()
 
    def join(self, user):
        if self.max_members and self.max_members < self.get_members_count():
            return
        self.members.add(user)
        self.save()
 
    def leave(self, user):
        self.members.remove(user)
        self.save()
 
    def __str__(self):
        return f"{self.name} ({self.get_members_count()})"
    

def file_upload_path(instance, filename):
    # Determine the file type based on the file extension
    file_extension = os.path.splitext(filename)[1].lower()

    # Choose the upload path based on the file type
    if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        return f'pictures/{filename}'
    elif file_extension in ['.mp4', '.avi', '.mkv']:
        return f'videos/{filename}'
    else:
        return f'other/{filename}'

class Message(models.Model):
    sender = models.ForeignKey(user, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='files')
    attachment = models.FileField(upload_to=file_upload_path, null=True)


