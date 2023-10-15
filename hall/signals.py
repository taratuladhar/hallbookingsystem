# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from django.core.mail import send_mail

@receiver(post_save, sender=Booking)
def send_email_on_status_change(sender, instance, created, **kwargs):
    if not created and instance.status != 'Pending':
        subject = 'Booking Status Changed'
        message = f'Your booking for {instance.program_title} has been changed to {instance.status}.'
        from_email = 'swetara88@gmail.com'  # Replace with your email
        recipient_list = [instance.email]  # Assuming 'email' is the recipient's email field in the Booking model
        send_mail(subject, message, from_email, recipient_list)
