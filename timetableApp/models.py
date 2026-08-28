from django.db import models
from classesApp.models import ClassRoom
from teachersApp.models import Teacher
from django.core.validators import MinValueValidator, MaxValueValidator

class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='timetables')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    period = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='timetables')
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('class_room', 'day', 'period')
        ordering = ['day', 'period']

    def __str__(self):
        return f"{self.class_room} - {self.day} - Period {self.period} - {self.subject}"
