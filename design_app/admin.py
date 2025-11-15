from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, DesignCategory, DesignRequest


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'fio', 'email', 'is_staff')
    list_filter = ('is_staff', 'username')
    search_fields = ('username', 'fio', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('fio', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'fio', 'email', 'password1', 'password2'),
        }),
    )

    ordering = ('username',)


@admin.register(DesignCategory)
class DesignCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'user__username', 'user__fio')
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'category', 'image')
        }),
        ('Статус и дополнительные данные', {
            'fields': ('status', 'admin_comment', 'design_image', 'created_at')
        }),
    )