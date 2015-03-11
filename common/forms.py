from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div


class LoginForm(forms.Form):
    user_name_email = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(self, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('user_name_email'),
                Field('password'),
                Submit('login', 'Login'),
            )
        )


class RegisterForm(forms.Form):
    user_name = forms.CharField(max_length=15)
    user_email = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())
    confpassword = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(self, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('user_name'),
                Field('user_email'),
                Field('password'),
                Field('confpassword'),
                Submit(name='register', value='Register'),
            )
        )
