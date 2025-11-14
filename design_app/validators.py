from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import DesignRequest
import os


def validate_image_size(value):
    if hasattr(value, 'size') and value.size > 2 * 1024 * 1024:
        raise ValidationError(_('Максимальный размер файла 2 МБ'))


def validate_image_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    if hasattr(value, 'name'):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise ValidationError(
                _('Неподдерживаемый формат изображения. Допустимые: %(formats)s'),
                params={'formats': ', '.join(valid_extensions)}
            )


def validate_required_field(value):
    if not value or (isinstance(value, str) and not value.strip()):
        raise ValidationError(_('Это поле обязательно для заполнения'))


def validate_status_change(instance):
    if instance.pk:
        try:
            old_instance = DesignRequest.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                if instance.status == 'completed' and not instance.design_image:
                    raise ValidationError({
                        'design_image': _('Для статуса "Выполнено" обязательно изображение дизайна')
                    })
                if instance.status == 'accepted' and not instance.admin_comment.strip():
                    raise ValidationError({
                        'admin_comment': _('Для статуса "Принято в работу" обязателен комментарий администратора')
                    })
        except DesignRequest.DoesNotExist:
            pass