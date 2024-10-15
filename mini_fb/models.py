# mini_fb/models.py
# Definte the data objects for our application
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    
    firstname = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.firstname} {self.lastname}' 
    
    def get_status_messages(self):
        return self.status_messages.all().order_by('-timestamp')
    
    def get_absolute_url(self):
        """
        Returns the URL to view this Profile object.
        """
        return reverse('show_profile', kwargs={'pk': self.pk})
    
class StatusMessage(models.Model):

    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f'Status by {self.profile}: {self.message[:50]}...'