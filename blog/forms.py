from django import forms
from django.conf import  settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, Div, Fieldset, Field
from sorl.thumbnail.fields import ImageFormField
from taggit.forms import TagField
from ckeditor.widgets import CKEditorWidget

from .models import Article


class BlogEntryForm(forms.Form):

    title = forms.CharField(max_length=150)
    image = ImageFormField()
    tags = TagField()
    content = forms.CharField(widget=CKEditorWidget())
    score = forms.DecimalField(max_value=settings.RATING_SCALE, max_digits=settings.RATING_MAX_DIGITS, min_value=0)

    def __init__(self, *args, **kwargs):
        super(BlogEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'pure-form pure-form-stacked pure-u-1'
        self.helper.layout = Layout(
            Div(
                Button('reset', 'Reset Section', data_section_id=1, data_btn_nm='reset', wrapper_class='rep', css_class='sec_btn pure-button'),
                Button('del', 'Delete Section', data_section_id=1, data_btn_nm='del', wrapper_class='rep', css_class='sec_btn pure-button'),
                Field('title', wrapper_class='rep pure-control-group', css_class='rep'),  # Class rep tells it is replicable item
                Field('score', wrapper_class='rep pure-control-group', css_class='rep'),  # Class rep tells it is replicable item
                Field('image', wrapper_class='norep pure-control-group', css_class='rep'),  # Class norep tells the item must be removed from replica's
                Field('content', wrapper_class='rep pure-control-group', css_class='rep'),
                css_class='section',
                css_id='sec',
                data_section_id=1
            ),
            Field('tags', wrapper_class='norep pure-control-group', css_class='norep'),
            ButtonHolder(
                Button('add', 'Add Section', data_btn_nm='add', data_section_count=1, css_id='add', css_class='sec_btn pure-button'),
                Button('save', 'Save Section', css_id='save', css_class='pure-button'),
                Submit('submit', 'Submit Post', css_id='submit', css_class='pure-button pure-button-primary'),
                css_id='buttons'
            ),
        )

    class Media:
        js = (
        )