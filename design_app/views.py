from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import DesignRequest, DesignCategory
from .forms import CustomUserCreationForm, LoginForm, DesignRequestForm


def index(request):
    """Главная страница"""
    completed_requests = DesignRequest.objects.filter(
        status='completed'
    ).order_by('-created_at')[:4]

    in_progress_count = DesignRequest.objects.filter(
        status='accepted'
    ).count()

    context = {
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count,
    }
    return render(request, 'design_app/index.html', context)


def register_view(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('design_app:profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):  # ← ИСПРАВЬ НАЗВАНИЕ НА login_view
    """Вход в систему"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.fio}!')
                return redirect('design_app:profile')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('design_app:index')


@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    user_requests = DesignRequest.objects.filter(user=request.user)
    return render(request, 'design_app/profile.html', {'user_requests': user_requests})