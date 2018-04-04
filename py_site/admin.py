from django.contrib import admin
from .models import Machine, User, Note


# Register your models here.

class MachineAdmin(admin.ModelAdmin):
    list_display = ('location', 'title')
    list_filter = ('location',)


class NoteAdmin(admin.ModelAdmin):
    list_display = ('machine', 'stop_equipment', 'date_start', 'text')


admin.site.register(Machine, MachineAdmin)
admin.site.register(User)
admin.site.register(Note, NoteAdmin)
