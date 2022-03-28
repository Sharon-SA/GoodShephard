from django import forms
from django.contrib.auth.models import User
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'date_of_birth')


class ClientForms(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'date_of_birth', 'gender', 'address',
                  'city', 'state', 'zip', 'email', 'phone', 'referred_by', 'reffered_to')


class InventoryForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('UPScode', 'item_description')


class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client', 'UPScode', 'item_description', 'request_quantity', 'delivered_quantity',
                  'date')
