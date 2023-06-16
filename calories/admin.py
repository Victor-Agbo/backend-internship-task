from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Entry)
admin.site.register(models.User)
