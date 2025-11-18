from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import DesignRequest, DesignCategory
from .forms import CustomUserCreationForm, LoginForm, DesignRequestForm, DesignCategoryForm


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def change_request_status(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        admin_comment = request.POST.get('admin_comment', '').strip()
        design_image = request.FILES.get('design_image')

        errors = {}

        if new_status in ['accepted', 'completed']:
            if new_status == 'accepted' and not admin_comment:
                errors['admin_comment'] = 'Для статуса "Принято в работу" обязателен комментарий'

            if new_status == 'completed' and not design_image:
                errors['design_image'] = 'Для статуса "Выполнено" обязательно изображение дизайна'

            if errors:
                for field, error in errors.items():
                    messages.error(request, error)
                return render(request, 'design_app/change_status.html', {'design_request': design_request})

            design_request.status = new_status
            design_request.admin_comment = admin_comment

            if new_status == 'completed' and design_image:
                design_request.design_image = design_image

            try:
                design_request.full_clean()
                design_request.save()
                messages.success(request, f'Статус заявки изменен на "{design_request.get_status_display()}"')
            except ValidationError as e:
                for field, error_list in e.message_dict.items():
                    for error in error_list:
                        messages.error(request, f'{field}: {error}')
        else:
            messages.error(request, 'Неверный статус')

        return redirect('design_app:admin_requests')

    return render(request, 'design_app/change_status.html', {'design_request': design_request})


@login_required
@user_passes_test(is_admin)
def manage_categories(request):
    if request.method == 'POST':
        if 'add_category' in request.POST:
            form = DesignCategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Категория добавлена')
            else:
                messages.error(request, 'Ошибка при добавлении категории')

        elif 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(DesignCategory, id=category_id)
            category_name = category.name
            category.delete()
            messages.success(request, f'Категория "{category_name}" удалена')

        return redirect('design_app:manage_categories')

    categories = DesignCategory.objects.all()
    form = DesignCategoryForm()
    return render(request, 'design_app/manage_categories.html', {
        'categories': categories,
        'form': form
    })

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