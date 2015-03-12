import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Hidden


EMAIL_REGEX = re.compile(r".*?@.*?\..*?")


def user_name_email(value):
    if EMAIL_REGEX.match(value):
        # User has supplied an email validate it
        validate_email(value)
    else:
        if len(value) > 30:
            raise ValidationError('User Name must be less than 15 chars')


class LoginForm(forms.Form):
    log_user_name_email = forms.CharField(max_length=255, label='User Name or Email', validators=[user_name_email, ])
    log_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('log_user_name_email', placeholder='Email or Username'),
                Field('log_password', placeholder='Password'),
                Hidden('formname', value='loginform'),
                Submit('login', 'Login'),
            )
        )

    def __str__(self):
        return 'loginform'


class RegisterForm(forms.Form):
    reg_user_name = forms.CharField(max_length=30)
    reg_user_email = forms.EmailField(label='Email')
    reg_password = forms.CharField(widget=forms.PasswordInput())
    reg_confpassword = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('reg_user_name', placeholder='User Name'),
                Field('reg_user_email', placeholder='Email'),
                Field('reg_password', placeholder='Password'),
                Field('reg_confpassword', placeholder='Confirm Password'),
                Hidden('formname', value='registerform'),
                Submit(name='register', value='Register'),
            )
        )

    def __str__(self):
        return 'registerform'
