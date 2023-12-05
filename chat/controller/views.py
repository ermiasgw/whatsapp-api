from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from chat.entity.models import ChatRoom
from chat.repository.serializers import ChatRoomSerializer
from rest_framework.permissions import IsAuthenticated

class ChatRoomLeaveView(generics.DestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        room_name = self.kwargs['room_name']
        user = self.request.user
        try:
            chatroom = ChatRoom.objects.get(name=room_name, members=user)
            chatroom.members.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ChatRoom.DoesNotExist:
            return Response({'detail': 'Chatroom not found or user is not a member.'}, status=status.HTTP_404_NOT_FOUND)
        
class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(members=[self.request.user])

class ChatRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]


class LeaveChatRoomAPIView(generics.UpdateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def update(self, request, *args, **kwargs):
        chatroom = self.get_object()
        user = request.user

        if user in chatroom.members.all():
            chatroom.members.remove(user)
            return Response({'detail': 'Successfully left the chatroom.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'You are not a member of this chatroom.'}, status=status.HTTP_400_BAD_REQUEST)