from django.contrib import admin

# Register your models here.

from . import models


class EntryAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.User)
