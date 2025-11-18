from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:product_id>/', views.start_chat, name='start_chat'),
    path('<int:conversation_id>/', views.chat_detail, name='chat_detail'),
    path('my/', views.my_chats, name='my_chats'),
]
