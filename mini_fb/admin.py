# mini_fb/admin.py
# tell the admin we want to administer these models
from django.contrib import admin
from .models import Profile, StatusMessage, Image, Friend 

# Register your models here.
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)