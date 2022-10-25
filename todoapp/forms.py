from django import forms
from django.contrib.auth.models import User
from todoapp.models import ToDos
from django.contrib.auth.forms import UserCreationForm


# class RegistrationForm(forms.Form):
#     first_name=forms.CharField()
#     last_name=forms.CharField()
#     username=forms.CharField()
#     email=forms.EmailField()
#     password=forms.CharField()   or

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2"
        ]
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


# class ToDoForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = [
#             "first_name",
#             "last_name",
#             "email",
#             "username",
#             "password"
#         ]

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDos
        fields = [
            "task_name"
        ]


class ToDoChangeForm(forms.ModelForm):
    class Meta:
        model = ToDos
        exclude = ("user",)
