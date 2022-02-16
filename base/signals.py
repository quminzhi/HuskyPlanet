from .models import User

from django.contrib.auth.signals import user_logged_in, user_logged_out

def login(sender, user, request, **kwargs):
    user.status = 1
    user.save()
    print(user.status)

def logout(sender, user, request, **kwargs):
    user.status = 0
    user.save()
    print(user.status)

user_logged_in.connect(login)
user_logged_out.connect(logout)
