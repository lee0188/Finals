from django import forms
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import collection_table

# YEARS= [x for x in range(1900,2100)]

# class PostForm(forms.Form):
#     cName = forms.CharField(max_length=4, initial='')
#     cSex = forms.CharField(max_length=1, initial='M')
#     cBirthday = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
#     cEmail = forms.EmailField(max_length=100, initial='', required=False)
#     cPhone = forms.CharField(max_length=10, initial='', required=False)
#     cAddr = forms.CharField(max_length=255, initial='', required=False)


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

# class collection_tableModelForm(forms.ModelForm):
#     class Meta:
#         model = collection_table
#         fields = ('__all__')




