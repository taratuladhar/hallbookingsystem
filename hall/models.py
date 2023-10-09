from django.db import models

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approve'),
        ('Rejected', 'Reject'),
    ]
     
    program_title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    email = models.EmailField()
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.program_title