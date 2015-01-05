from django.contrib import admin
from staff.models import Staff, Permission

admin.site.register(Permission)
admin.site.register(Staff)