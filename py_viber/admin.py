from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'viber_id', 'role')


admin.site.register(User, UserAdmin)
