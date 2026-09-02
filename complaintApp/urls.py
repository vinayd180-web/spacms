from django.urls import path
from . import views

urlpatterns = [
    path('file/', views.file_complaint, name='file_complaint'),
    path('my/', views.my_complaints, name='my_complaints'),
    path('all/', views.all_complaints, name='all_complaints'),
    path('resolve/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
]
