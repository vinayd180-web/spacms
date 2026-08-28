from django.urls import path
from . import views

urlpatterns = [
    path('', views.backup_data, name='backup_data'),
]
