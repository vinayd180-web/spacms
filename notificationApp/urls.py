from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_notification, name='send_notification'),
    path('my/', views.my_notifications, name='my_notifications'),
]
