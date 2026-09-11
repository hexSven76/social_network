from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegisterationForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'example@mail.domain'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'your password'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'your password again'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This Email Already Exists!')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('This username Already Exists!')
        return username
    
    # overriding clean() for custom validation (password = confirm password)
    def clean(self):
        cd = super().clean()
        pw1 = cd.get('password1')
        pw2 = cd.get('password2')
        if pw1 and pw2: # checking if they exist
            if pw1 != pw2:
                raise ValidationError('Passwords must match!')
