from django.contrib import admin

# Register your models here.

from .models import Room, Message, Topic, User

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
