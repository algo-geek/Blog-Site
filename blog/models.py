from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import *

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=300)
    occupation = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    dp = models.ImageField(upload_to = 'dp', null= True, blank=True, default='/dp/luna.jpg')
    prof_user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.prof_user.username) + " " + str(self.name)


class Post(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'post', null= True, blank=True)
    def __str__(self):
        return str(self.title) + " " + str(self.author)



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(prof_user=instance)

post_save.connect(create_user_profile, sender=User)   

       