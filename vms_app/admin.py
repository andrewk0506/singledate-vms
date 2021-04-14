from django.contrib import admin
from .models.log import Log
from .models import Role, Site, Staff

# Register your models here.
admin.site.register(Log)
admin.site.register(Role)
admin.site.register(Site)
admin.site.register(Staff)

