from django import forms
from .models import Booking, Feedback
from hall import models

class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['status']

class FeedbackForm(forms.ModelForm):
    by = forms.CharField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Feedback
        fields = ['by', 'message']