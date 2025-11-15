from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, DesignRequest


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    fio = forms.CharField(max_length=255, label='ФИО')

    agree_to_terms = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных',
        error_messages={'required': 'Необходимо принять соглашение'}
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError({
                'password2': 'Пароли не совпадают'
            })

        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ('fio', 'username', 'email', 'password1', 'password2')


class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'image']


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')