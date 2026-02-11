from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Логин',
            'email': 'Email адрес',
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio'] # ВАЖНО: Тут должно быть имя поля из models.py
        labels = {
            'avatar': 'Фото профиля',
            'bio': 'О себе',
        }