from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name="home"),
    path('chat/<username>/', views.get_or_create_chatroom,name="chatroom"),
    path('chat/room/<chatroom_name>',views.chat_view,name="chatroom"),
]