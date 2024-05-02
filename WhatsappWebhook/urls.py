from django.urls import path
from .views import whatsAppWebhook

urlpatterns = [
    path('',view = whatsAppWebhook, name= 'webhook'),
]


# VERIFY_TOKEN = 'e58b84b9-3017-4d13-be4e-04c05e50a353'
