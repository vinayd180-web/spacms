from django.db import models

class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField(default=25)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Course fees for this class")

    def __str__(self):
        return f"{self.name} - {self.section}"

class Subjects(models.Model):
    subject = models.CharField(max_length=50)

    def __str__(self):
        return self.subject

