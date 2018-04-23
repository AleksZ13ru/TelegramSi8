from django.contrib import admin
from .models import User, Message


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'viber_id', 'role')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'date_status', 'text', 'key')
    list_filter = ('user', 'status')


admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
