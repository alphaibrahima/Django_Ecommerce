from dataclasses import field
from logging import PlaceHolder
from django import forms
from .models import Account



class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Entrer votre prenom',
        'class':'form-control',

    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Entrer votre nom',
        'class':'form-control',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder':'Entrer votre adresse email',
        'class':'form-control',
    }))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder':'Entrer votre numero de telephone',
        'class':'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Entrer votre mot de passe',
        'class':'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Entrer votre mot de passe',
        'class':'form-control',
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('password dose not match')