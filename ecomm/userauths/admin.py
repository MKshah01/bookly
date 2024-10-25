from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']  # Use proper quotes and field names

admin.site.register(User, UserAdmin)  # Correct the registration