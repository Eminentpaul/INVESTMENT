from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction, Investment, User


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'image']


class InvestmentForm(ModelForm):
    class Meta:
        model = Investment
        fields = ['amount']


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        # widgets = {
        #     'username': forms.TextInput(attrs={"placeholder":"Enter Username"}),
        #     'email': forms.EmailInput(attrs={"placeholder": "Enter Your Email"}),
        #     'first_name': forms.TextInput(attrs={"placeholder":"Enter Your First Name"}),
        #     'last_name': forms.TextInput(attrs={"placeholder":"Enter Your Last Name"}),
        #     'password1': forms.TextInput(attrs={"placeholder":"Enter Your Password"}),
        #     'password2': forms.PasswordInput(attrs={"placeholder":"Confirm Password"}),
        # }


class UserForm2(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'image']
        # widgets = {
        #     'username': forms.TextInput(attrs={"placeholder":"Enter Username"}),
        #     'email': forms.EmailInput(attrs={"placeholder": "Enter Your Email"}),
        #     'first_name': forms.TextInput(attrs={"placeholder":"Enter Your First Name"}),
        #     'last_name': forms.TextInput(attrs={"placeholder":"Enter Your Last Name"}),
        #     'password1': forms.TextInput(attrs={"placeholder":"Enter Your Password"}),
        #     'password2': forms.PasswordInput(attrs={"placeholder":"Confirm Password"}),
        # }