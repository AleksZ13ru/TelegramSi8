from django.contrib import admin
from .models import Folder, File
from .models import Value, Date,Party, Machine, ValueChange, ComPort


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'parsing_status')
    list_filter = ('path', 'parsing_status')


class ValueAdmin(admin.ModelAdmin):
    list_display = ('display_title', 'register', 'date', 'display_len')
    list_filter = ('register', 'date')


class ValueChageAdmin(admin.ModelAdmin):
    list_display = ('machine', 'read_datetime', 'read_value')


class MachineAdmin(admin.ModelAdmin):
    list_display = ('title', 'enable', 'register', 'com_port')
    list_filter = ('title', 'enable', 'register', 'com_port')


class MachineInline(admin.TabularInline):
    model = Machine
    extra = 0
    can_delete = False
    fields = ('title', 'enable', 'register')


class ComPortAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'port_name', 'timeout')
    inlines = [MachineInline]


admin.site.register(Folder)
admin.site.register(File, FileAdmin)

admin.site.register(ComPort, ComPortAdmin)
admin.site.register(Value, ValueAdmin)
admin.site.register(ValueChange, ValueChageAdmin)
admin.site.register(Date)
admin.site.register(Party)
admin.site.register(Machine, MachineAdmin)
