from django.contrib import admin
from .models import Startup, Service, Technology

# Register your models here.
admin.site.register(Startup)
admin.site.register(Service)
admin.site.register(Technology)
