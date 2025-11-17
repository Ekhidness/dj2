from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    fio = models.CharField(verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='Email')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.fio} ({self.username})"


class DesignCategory(models.Model):
    name = models.CharField(verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория дизайна'
        verbose_name_plural = 'Категории дизайна'


class DesignRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('accepted', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='design_requests'
    )
    title = models.CharField(verbose_name='Название заявки')
    description = models.TextField(verbose_name='Описание заявки')
    category = models.ForeignKey(
        DesignCategory,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    image = models.ImageField(
        upload_to='request_images/',
        verbose_name='Изображение помещения'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус заявки'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    admin_comment = models.TextField(
        blank=True,
        verbose_name='Комментарий администратора'
    )
    design_image = models.ImageField(
        upload_to='design_images/',
        blank=True,
        null=True,
        verbose_name='Изображение дизайна'
    )

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def can_be_deleted(self):
        return self.status == 'new'

    def clean(self):
        if self.status == 'completed' and not self.design_image:
            raise ValidationError({
                'design_image': 'Для статуса "Выполнено" обязательно изображение дизайна'
            })
        if self.status == 'accepted' and not self.admin_comment.strip():
            raise ValidationError({
                'admin_comment': 'Для статуса "Принято в работу" обязателен комментарий'
            })

    class Meta:
        verbose_name = 'Заявка на дизайн'
        verbose_name_plural = 'Заявки на дизайн'
        ordering = ['-created_at']