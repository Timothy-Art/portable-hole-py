from django.contrib import admin
from . import models

admin.site.register(models.System)
admin.site.register(models.Type)
admin.site.register(models.Category)
admin.site.register(models.Item)
admin.site.register(models.PortableHole)
admin.site.register(models.UserItem)
