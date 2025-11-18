from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, DesignRequest, DesignCategory
import os
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        help_text='Введите действующий email адрес'
    )
    fio = forms.CharField(
        max_length=255,
        label='ФИО',
        help_text='Только кириллические буквы, дефис и пробелы'
    )
    agree_to_terms = forms.BooleanField(
        required=True,
        label='Согласие на обработку персональных данных',
        help_text='Для регистрации необходимо принять соглашение'
    )

    def clean_fio(self):
        fio = self.cleaned_data.get('fio')
        if fio and not re.match(r'^[а-яА-ЯёЁ\s\-]+$', fio):
            raise ValidationError('ФИО может содержать только кириллические буквы, дефис и пробелы')
        return fio

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and not re.match(r'^[a-zA-Z\-]+$', username):
            raise ValidationError('Логин может содержать только латинские буквы и дефис')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов')
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError({'password2': 'Пароли не совпадают'})

        return cleaned_data

    class Meta:
        model = CustomUser
        fields = ('fio', 'username', 'email', 'password1', 'password2')
        help_texts = {
            'fio': 'Только кириллица, дефис и пробелы.',
            'username': 'Только латиница и дефис. Будет использоваться для входа.',
            'email': 'Введите действующий email адрес.',
            'password1': 'Минимум 8 символов.',
            'password2': 'Введите пароль еще раз для подтверждения.',
        }


class DesignRequestForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        return description

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
        help_texts = {
            'title': 'Краткое описание заявки',
            'description': 'Подробное описание помещения и ваших пожеланий',
            'category': 'Выберите подходящую категорию дизайна',
            'image': 'Форматы: JPG, JPEG, PNG, BMP. Максимальный размер: 2 МБ',
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        help_text='Введите ваш логин'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Пароль',
        help_text='Введите ваш пароль'
    )


class DesignCategoryForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name

    class Meta:
        model = DesignCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название категории'})
        }
        help_texts = {
            'name': 'Введите название новой категории',
        }