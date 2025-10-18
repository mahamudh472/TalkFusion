from django.urls import path
from . import views
from .webhook import webhook, fb_webhook

urlpatterns = [
    path('send_whatsapp_message/', views.SendWhatsappMessageView.as_view(), name='send_whatsapp_message'),
    path('webhook/whatsapp/', webhook, name='whatsapp_webhook'),
    path('webhook/facebook/', fb_webhook, name='facebook_webhook'),
    path('test', views.custom_view, name='custom_view'),
]