from django.urls import path
from . import views

urlpatterns = [
    path('test-chat/', views.test_chat, name='test_chat'),
    path('health/', views.health_check, name='health_check'),
    path('webhook/', views.whatsapp_webhook, name='whatsapp_webhook'),
]