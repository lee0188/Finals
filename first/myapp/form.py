from django import forms
from datetime import datetime

YEARS= [x for x in range(1900,2100)]

class PostForm(forms.Form):
    cName = forms.CharField(max_length=4, initial='')
    cSex = forms.CharField(max_length=1, initial='M')
    cBirthday = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
    cEmail = forms.EmailField(max_length=100, initial='', required=False)
    cPhone = forms.CharField(max_length=10, initial='', required=False)
    cAddr = forms.CharField(max_length=255, initial='', required=False)