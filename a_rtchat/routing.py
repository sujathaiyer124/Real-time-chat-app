from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/chatroom/<chatroom_name>/", consumers.ChatroomConsumer.as_asgi()),
    path("ws/private-chat/<user_id>/", consumers.PrivateChatConsumer.as_asgi()),
]