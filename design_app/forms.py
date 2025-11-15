from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, DesignRequest
import os


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    fio = forms.CharField(max_length=255, label='ФИО')
    agree_to_terms = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных'
    )

    class Meta:
        model = CustomUser
        fields = ('fio', 'username', 'email', 'password1', 'password2')


class DesignRequestForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise ValidationError('Максимальный размер файла 2 МБ')

            valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError('Неподдерживаемый формат изображения')

        return image

    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'image']


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')