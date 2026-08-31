from django.db import models
from classesApp.models import ClassRoom
from accountsApp.models import User

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True)
    is_for_all = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
