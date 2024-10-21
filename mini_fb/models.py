# mini_fb/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Profile Model (Unchanged)
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
        return reverse('show_profile', kwargs={'pk': self.pk})

class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f'Status by {self.profile}: {self.message[:50]}...'
    
    def get_images(self):
        return self.images.all()


class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')  
    timestamp = models.DateTimeField(auto_now_add=True)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'Image for {self.status_message} uploaded at {self.timestamp}'
