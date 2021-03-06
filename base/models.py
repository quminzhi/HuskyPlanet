from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
# from django.contrib.auth.models import User

# TODO: Customize User Model
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True)
    status = models.IntegerField(null=False, default=0)
    
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    # when creating superuser, comment out following code
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) # save timestamp when it is created

    class Meta:
        ordering = ['-updated', '-created'] # in descending order

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) # save timestamp when it is created
    
    class Meta:
        ordering = ['-updated', '-created'] # in descending order
    
    def __str__(self):
        return self.body[0:50]