from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',)
    list_display = ('username', 'email')

admin.site.register(User, UserAdmin)
