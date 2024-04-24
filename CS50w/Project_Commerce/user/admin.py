# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

# Import your CustomUser model
from .models import CustomUser

# Define a custom admin class for the Group model
class CustomGroupAdmin(GroupAdmin):
    filter_horizontal = ('permissions',)  # Optionally customize permissions display

# Unregister the default GroupAdmin
admin.site.unregister(Group)

# Register the Group model with the custom admin class
admin.site.register(Group, CustomGroupAdmin)
