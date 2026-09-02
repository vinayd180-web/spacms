from django.db import models
from classesApp.models import ClassRoom
from teachersApp.models import Teacher

class LiveClass(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='live_classes')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='live_classes')
    meeting_link = models.URLField(max_length=500)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return self.title
