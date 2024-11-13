from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email", max_length=150)

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        # 这里可以添加额外的登录验证逻辑