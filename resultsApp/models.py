from django.db import models
from studentsApp.models import Student
from examsApp.models import Exam
from django.core.validators import MinValueValidator, MaxValueValidator

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    marks = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    grade = models.CharField(max_length=5, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'exam')  # एक student के एक exam में सिर्फ एक marks entry

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.marks}"
