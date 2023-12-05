"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from chat.controller.views import  LeaveChatRoomAPIView, ChatRoomDetailView, ChatRoomListCreateView, ChatRoomLeaveView
from drf_spectacular.views import SpectacularAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom-list'),
    path('api/chatrooms/<str:room_name>/', ChatRoomDetailView.as_view(), name='chatroom-detail'),
    path('api/chatrooms/<str:room_name>/leave/', ChatRoomLeaveView.as_view(), name='chatroom-leave'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),



]
