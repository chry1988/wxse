from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import wxseUser

admin.site.register(wxseUser, UserAdmin)