# hall/models.py
from django.db import models

class Booking(models.Model):
    program_title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.program_title
