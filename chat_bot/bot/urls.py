# bot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.llama_bot, name='llama_bot'),
    path('chat/', views.chatbot_view, name='chatbot'),
]
