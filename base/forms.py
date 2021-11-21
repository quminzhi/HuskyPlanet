from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm

# create model form for Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        # fields = ['host', 'name'] # customize
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
