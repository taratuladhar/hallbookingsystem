from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approve'),
        ('Rejected', 'Reject'),
    ]
     
    program_title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField(default='00:00:00')
    end_time = models.TimeField()
    email = models.EmailField(default='00:00:00')
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.program_title
    
    
class Feedback(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=40)
    message=models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.by