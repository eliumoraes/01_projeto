from django.contrib import admin

from .models import *

admin.site.register(Cliente)
admin.site.register(UserRole)
admin.site.register(UserProfile)