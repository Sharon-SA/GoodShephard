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
        model = Inventory
        fields = ('UPScode', 'item_description', 'total_quantity')




class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client', 'UPScode', 'item_description', 'request_quantity', 'delivered_quantity',
                  'date')

class OrdereditForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client','item_description', 'request_quantity', 'delivered_quantity',
                  'date')


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'date_of_birth', 'address', 'city', 'state', 'zip']

