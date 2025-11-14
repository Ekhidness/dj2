from django.contrib import admin

from design_app.models import DesignCategory, DesignRequest, CustomUser

# Register your models here.
admin.site.register(DesignCategory)
admin.site.register(DesignRequest)
admin.site.register(CustomUser)