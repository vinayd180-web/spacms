from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_fees, name='student_fees'),
    path('pay-now/', views.payment_gateway, name='payment_gateway'),
    path('id-card/', views.student_id_card, name='student_id_card'),
    path('admin/list/', views.admin_fees_list, name='admin_fees_list'),
    path('admin/id-cards/', views.admin_student_id_cards, name='admin_student_id_cards'),
    path('admin/id-card/<int:student_id>/', views.admin_student_id_card_detail, name='admin_student_id_card_detail'),
    path('admin/update/<int:fees_id>/', views.admin_fees_update, name='admin_fees_update'),
]
