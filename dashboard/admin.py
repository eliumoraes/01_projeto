from django.contrib import admin

from .models import *

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'phone', 'email', 'date_created', 'div_id')

admin.site.register(UserRole)
admin.site.register(UserProfile)
admin.site.register(ClientCategory)
admin.site.register(ClientCategoryRelation)
admin.site.register(CategoryVersion)
admin.site.register(ClientCategoryVersion)

@admin.register(ClientBackup)
class ClientBackup(admin.ModelAdmin):
    list_display = ('client', 'solic_date', 'solic_version', 'solic_user', 'atend_date', 'atend_user', 'status', 'localizacao')

admin.site.register(BackupDestination)