
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from django.forms import widgets

class CreateUserForm(UserCreationForm):

    class Meta:
        
        model = User

        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):

        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    
    def clean_email(self):

        email = self.cleaned_data.get('email')

        if User.objects.filter(email = email).exists():

            raise forms.ValidationError('User with this email already exists.')

        if len(email) > 350:

            raise forms.ValidationError('Your email length should be less than 350 characters.')

        return email


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=widgets.TextInput())

    password = forms.CharField(widget=widgets.PasswordInput())


class UpdateUserForm(forms.ModelForm):

    class Meta:

        model = User

        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):

        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if User.objects.filter(email = email).exclude(pk=self.instance.pk).exists():
            
            raise forms.ValidationError('User with this email already exists.')

        if len(email) > 350:

            raise forms.ValidationError('Your email length should be less than 350 characters.')

        return email


