from django.contrib import admin

# Register your models here.
from mock_service import models

admin.site.register(models.MockProject)
admin.site.register(models.MockUnit)

