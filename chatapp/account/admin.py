from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Account

admin.site.register(Account, UserAdmin)
