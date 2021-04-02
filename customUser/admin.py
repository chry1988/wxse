from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import wxseUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class wxUserAdmin(UserAdmin):
    model = wxseUser

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ['userDepartment', 'userGroup', 'userPrivilege', 'userPhone']

admin.site.register(wxseUser, wxUserAdmin)