import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Hidden, HTML
from sorl.thumbnail.fields import ImageFormField

from .models import CustomUser, ContactUs


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
    log_password = forms.CharField(widget=forms.PasswordInput(), label='Password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('log_user_name_email', placeholder='Email or Username'),
                Field('log_password', placeholder='Password'),
                Hidden('formname', value='loginform'),
                Submit('login', 'Login', css_class='pure-button'),
            )
        )

    def __str__(self):
        return 'loginform'


class RegisterForm(forms.Form):
    reg_user_name = forms.CharField(max_length=30, label='User Name')
    reg_user_email = forms.EmailField(label='Email')
    reg_password = forms.CharField(widget=forms.PasswordInput(), label='Password', min_length=6)
    reg_confpassword = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password', min_length=6)

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
                Submit(name='register', value='Register', css_class='pure-button'),
            )
        )

    def clean_reg_user_email(self):
        username = self.cleaned_data['reg_user_name']
        email = self.cleaned_data['reg_user_email']
        user = CustomUser.objects.get_by_user_or_email(username, email)
        if user:
            raise ValidationError('User with Username & Email is already in use')

    def clean_reg_confpassword(self):
        conf_password = self.cleaned_data['reg_confpassword']
        password = self.cleaned_data['reg_password']
        if password != conf_password:
            raise ValidationError('Password & Confirm passwords do not match!')

    def __str__(self):
        return 'registerform'


class ProfileForm(forms.Form):
    choices = (
        ('N', 'No Thanks'), ('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')
    )

    avatar = ImageFormField(required=False)
    name = forms.CharField(max_length=50, required=False)
    location = forms.CharField(max_length=20, required=False)
    about = forms.CharField(widget=forms.Textarea(), max_length=1000, required=False)
    subscription = forms.ChoiceField(choices=choices, label='Subscribe to Updates')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML("""<div class='avatar'>{% load thumbnail %}{{ form.avatar }}{% if form.avatar.value %}{% thumbnail form.avatar.value "300x200" as im %}<img src='{{ im.url }}{% endthumbnail %}'>{% endif %}></div>"""),
                css_class='pure-u-1 pure-u-md-6-12 pure-u-lg-5-12 ls'
            ),
            Div(
                Field('name'),
                Field('location'),
                Field('about'),
                Field('subscription'),
                Hidden('username', value=self.initial['username']),
                css_class='pure-u-1 pure-u-md-6-12 pure-u-lg-7-12 rs'
            ),
            Submit(name='save', value='Save', css_class='pure-button'),
        )


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        exclude = ['contacted_date_time', 'contacted_by']

    def __init__(self, *args, **kwargs):
        super(ContactUsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='pure-button pure-button-primary'))
