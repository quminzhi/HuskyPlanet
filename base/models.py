from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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
    
    def __str__(self):
        return self.body[0:50]