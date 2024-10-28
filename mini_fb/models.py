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

    def get_friends(self):
        friends = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)
        friend_profiles = []
        for friend in friends:
            if friend.profile1 == self:
                friend_profiles.append(friend.profile2)
            else:
                friend_profiles.append(friend.profile1)
        return friend_profiles

    def add_friend(self, other):
        if self == other:
            return
        
        existing_friendship = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) |
            models.Q(profile1=other, profile2=self)
        ).exists()

        if not existing_friendship:
            
            Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        current_friends = self.get_friends()
        suggested_profiles = Profile.objects.exclude(id=self.id).exclude(id__in=[friend.id for friend in current_friends])

        return suggested_profiles
    
    def get_news_feed(self):
        friends = self.get_friends()
        profiles = [self] + friends
        
        return StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')
    
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
    

class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.profile1.firstname} {self.profile1.lastname} & {self.profile2.firstname} {self.profile2.lastname}'