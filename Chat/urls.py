from django.contrib.auth import logout

from django.urls import path
from .views import *

app_name = 'Chat'
urlpatterns = [
    path('', index, name='index'),
    path('chat/', chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', message_list, name='message-detail'),
    path('api/messages/', message_list, name='message-list'),
    path('logout/', logout, {'next_page': 'index'}, name='logout'),
    path('users/', users, name='users'),
    path('users/', users_nav, name='users_nav')

]
