from django.urls import path
from . import views

urlpatterns = [
    path('broadcast/', views.broadcast, name='broadcast'),
]
