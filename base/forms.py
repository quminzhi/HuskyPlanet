from django.forms import ModelForm
from .models import Room

# create model form for Room
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        # fields = ['host', 'name'] # customize