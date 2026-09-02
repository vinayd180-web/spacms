from django.db import models
from accountsApp.models import User
from studentsApp.models import Student

class Fees(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Total course fees")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Paid amount")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.amount} - {self.status}"
