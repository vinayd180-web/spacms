from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.update_profile, name='update_profile'),
    path('', views.my_profile, name='my_profile'),
]
