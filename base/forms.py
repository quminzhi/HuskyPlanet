from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

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
        fields = ['username', 'email']