from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import wxseUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = wxseUser
        fields = ('username', 'email', 'userDepartment', 'userGroup', 'userPrivilege', 'userPhone')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = wxseUser
        fields = UserChangeForm.Meta.fields
