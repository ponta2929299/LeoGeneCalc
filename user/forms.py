import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

#既存のUserモデルを使用
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="名前",max_length=30, required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(label="パスワード",widget=forms.PasswordInput(attrs={"class":"form-control"}),required=True)
    password2 = forms.CharField(label="確認用パスワード",widget=forms.PasswordInput(attrs={"class":"form-control"}),required=True)
    
    class Meta:
        model = User
        fields = ["username","password1","password2"]