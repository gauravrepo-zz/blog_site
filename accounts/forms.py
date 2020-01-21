from django import forms
from .models import Account
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404


# Registeration form
class RegisterationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'username_error' : "Username already exists, try another",
        'email_error' : "Email already exists, try another"
    }

    email           = forms.EmailField(max_length=60, required=True, help_text="Add a valid email address")
    username        = forms.CharField(label="Username", max_length=30, required=True)
    first_name      = forms.CharField(label="First Name", max_length=30)
    last_name       = forms.CharField(label="Last Name", max_length=30)
    password1       = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2       = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, help_text="Enter the same password as above, for verification.")

    class Meta:
        model = Account
        fields = ("email", "username","first_name", "last_name", "password1", "password2")
    
    def clean(self):
        password1   = self.cleaned_data["password1"]
        password2   = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
    
    def clean_email(self):
        email       = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(id=self.instance.id).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(
                self.error_messages['email_error'],
                code='email_error',
            )
        return email
    
    def clean_username(self):
        username    = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(id=self.instance.id).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(
                self.error_messages['username_error'],
                code='username_error',
            )
    
    def save(self, commit=True):
        user = super(RegisterationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        
        if commit:
            user.save()
        return user

# Login form
class LoginForm(forms.Form):
    error_messages = {
        'login_error': "Invalid login credentials.",
    }

    email       = forms.EmailField(max_length=60, required=True, help_text="Enter your register email address")
    password    = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    class Meta:
        fields = ("email", "password")
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        return email

    def clean_password(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError(self.error_messages['login_error'], code='login_error' )
        return password


# Update account form

class UpdateAccountForm(forms.ModelForm):
    error_messages = {
        'username_error' : "Username already exists, try another",
    }
    username        = forms.CharField(label="Username", max_length=30, required=True)
    first_name      = forms.CharField(label="First Name", max_length=30)
    last_name       = forms.CharField(label="Last Name", max_length=30)
    image           = forms.ImageField(label="Profile Image", required=False)
    
    class Meta:
        fields = ("username", "first_name", "last_name", "image")
        model = Account

    def clean_username(self):
        username    = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(id=self.instance.id).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(
                self.error_messages['username_error'],
                code='username_error',
            )

    def save(self, commit=True):
        account                 = get_object_or_404(Account, email=self.instance.email)
        account.username        = self.cleaned_data['username']
        account.first_name      = self.cleaned_data['first_name']
        account.last_name       = self.cleaned_data['last_name']

        if self.cleaned_data['image']:
            account.image      = self.cleaned_data['image']

        if commit:
            account.save()
        return account