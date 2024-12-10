# forms.py

from django import forms
from .models import Photo
from .models import Photoshoot
from django.contrib.auth.models import User

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'price']  # Include the fields you want to edit



class PhotoshootBookingForm(forms.ModelForm):
    class Meta:
        model = Photoshoot
        fields = ['title', 'description', 'date', 'location']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username': None,  # Remove the help text for the username field
        }