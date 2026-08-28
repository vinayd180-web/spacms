from django.db import models
from teachersApp.models import Teacher
from classesApp.models import ClassRoom

class WorkLog(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='worklogs')
    date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField()
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=100)
    syllabus_covered = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-in_time']

    @property
    def total_time(self):
        # Calculate total time in hours
        from datetime import datetime, timedelta
        fmt = '%H:%M'
        t1 = datetime.strptime(str(self.in_time), fmt)
        t2 = datetime.strptime(str(self.out_time), fmt)
        delta = t2 - t1
        return delta

    def __str__(self):
        return f"{self.teacher} - {self.date} - {self.subject}"
