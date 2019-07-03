from django.contrib import admin
from .models import Folder, File
from .models import Value, Date, Machine, ValueChange, ComPort


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'parsing_status')
    list_filter = ('path', 'parsing_status')


class ValueAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'register', 'date', 'display_len')
    list_filter = ('register', 'date')


class ValueChageAdmin(admin.ModelAdmin):
    list_display = ('machine', 'read_datetime', 'read_value')


class MacineAdmin(admin.ModelAdmin):
    list_display = ('title', 'register', 'com_port')
    list_filter = ('title', 'register', 'com_port')


admin.site.register(Folder)
admin.site.register(File, FileAdmin)

admin.site.register(ComPort)
admin.site.register(Value, ValueAdmin)
admin.site.register(ValueChange, ValueChageAdmin)
admin.site.register(Date)
admin.site.register(Machine, MacineAdmin)
