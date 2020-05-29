from django.contrib import admin

from .models import *

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'phone', 'email', 'date_created', 'div_id')
admin.site.register(UserRole)
admin.site.register(UserProfile)
admin.site.register(ClientCategory)
admin.site.register(ClientCategoryRelation)