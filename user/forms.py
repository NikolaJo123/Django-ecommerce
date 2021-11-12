import django
from django.db.models import fields
from django.forms import ModelForm, TextInput, Textarea, widgets, EmailField, EmailInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import Select, FileInput
from django.contrib.auth.models import User
from user.models import UserProfile






class SignUp_Form(UserCreationForm):
    '''username = forms.CharField(max_length=50, label= 'User Name:')
    first_name = forms.CharField(max_length=100,  label= 'First_name:')
    last_name = forms.CharField(max_length=100,  label= 'Last_name:')
    email = forms.EmailField(max_length=300, label= 'Email:')'''


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        labels = {'first_name': '', 'last_name': '', 'username': '', 'email': '', 'password1':'', 'password2':  ''}
        widgets = {
            'first_name' : forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'First Name',}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'last Name'}),
            'username' : forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'Username'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'Email Address'}),
            'password1' : forms.PasswordInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'Password'}),
            'password2' : forms.PasswordInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'Password Confirmation'}),
        }



class UserUpdateForm(UserChangeForm):
    def clean_password(self):
        return ""
    class Meta:
        model = User
        fields=('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'username'}),
            'first_name': TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'last_name'}),
            'email': EmailInput(attrs={'class': 'form-control rounded-left', 'palceholder': 'myemail@mail.com'}),
        }

CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('New York', 'New York'),
]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country', 'image', 'language')
        widgets = {
            'phone': TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'address'}),
            'city': Select(attrs={'class': 'form-control rounded-left', 'placeholder': 'city'}, choices=CITY),
            'country': TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'country'}),
            'image': FileInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'iamge'}),
        }
        