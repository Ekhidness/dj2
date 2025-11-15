from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DesignRequest
from .forms import CustomUserCreationForm, LoginForm, DesignRequestForm


def index(request):
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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('design_app:profile')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('design_app:index')


@login_required
def profile_view(request):
    user_requests = DesignRequest.objects.filter(user=request.user)
    return render(request, 'design_app/profile.html', {'user_requests': user_requests})


@login_required
def create_request_view(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('design_app:profile')
    else:
        form = DesignRequestForm()

    return render(request, 'design_app/create_request.html', {'form': form})


@login_required
def delete_request_view(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id, user=request.user)

    if design_request.can_be_deleted():
        design_request.delete()
        messages.success(request, 'Заявка удалена')
    else:
        messages.error(request, 'Невозможно удалить заявку')

    return redirect('design_app:profile')