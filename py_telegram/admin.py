from django.contrib import admin

from .models import User, Favorite, Loop, Message


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'telegram_id', 'role')
    # list_filter = 'role'


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'date_status', 'text')
    list_filter = ('user', 'status')


admin.site.register(User, UserAdmin)
admin.site.register(Favorite)
admin.site.register(Loop)
admin.site.register(Message, MessageAdmin)
