from django import forms
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

    def __init__(self, *args, **kwargs):
        super(BlogEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Button('reset', 'Reset Section', data_section_id=1, data_btn_nm='reset', css_class='sec_btn rep'),
                Button('del', 'Delete Section', data_section_id=1, data_btn_nm='del', css_class='sec_btn rep'),
                Field('title', css_class='rep'),  # Class rep tells it is replicable item
                Field('image', css_class='norep'),  # Class norep tells the item must be removed from replica's
                Field('content', css_class='rep'),
                Button('reset', 'Reset Section', data_section_id=1, data_btn_nm='reset', css_class='sec_btn rep'),
                Button('del', 'Delete Section', data_section_id=1, data_btn_nm='del', css_class='sec_btn rep'),
                css_class='section',
                css_id='sec_1'
            ),
            Field('tags'),
            ButtonHolder(
                Button('add', 'Add Section', data_section_count=1, css_id='add'),
                Button('save', 'Save Section', css_id='save'),
                Submit('submit', 'Submit Post', css_id='submit'),
                css_id='buttons'
            ),
        )

    class Media:
        js = (
        )