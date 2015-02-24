from django import forms
from django.conf import  settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, Div, Fieldset, Field, Hidden
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


class BlogEntryUpdateForm(forms.Form):
    def __new__(cls, *args, **kwargs):
        """
        Add sections dynamically
        :param cls:
        :param args:
        :param kwargs:
        :return:
        """
        new_class = super(BlogEntryUpdateForm, cls).__new__(cls, *args, **kwargs)
        data = kwargs.get('initial')
        base_fields = {}
        for section in data:
            delim = '' if section.section_order == 1 else '_' + str(section.section_order)
            base_fields['title' + delim] = forms.CharField(max_length=150, initial=section.title)
            base_fields['content' + delim] = forms.CharField(widget=CKEditorWidget(), initial=section.content)
            base_fields['score' + delim] = forms.DecimalField(max_value=settings.RATING_SCALE, max_digits=settings.RATING_MAX_DIGITS, min_value=0, initial=section.score)
            base_fields['id' + delim] = forms.IntegerField(initial=section.id)

            if section.section_order == 1:
                base_fields['image'] = ImageFormField(initial=section.article.image)
                base_fields['article'] = forms.IntegerField(initial=section.article_id)
                # base_fields['tags' + delim] = TagField(section.article.tags)
        new_class.base_fields = base_fields

        return new_class

    def __init__(self, *args, **kwargs):
        super(BlogEntryUpdateForm, self).__init__(*args, **kwargs)
        # Field mappings for dynamic generation
        self.helper = FormHelper()
        self.helper.form_class = 'pure-form pure-form-stacked pure-u-1'
        data = kwargs.pop('initial')
        # Explicitly initializing form to handle edits
        #if not self.is_bound:
        self.initial = {}

        layouts = []
        artcle_id = 0
        for section in data:
            if section.section_order == 1:
                artcle_id = section.article_id
                layouts.append(
                    Div(
                        Field('title', wrapper_class='rep pure-control-group', css_class='rep'),  # Class rep tells it is replicable item
                        Field('score', wrapper_class='rep pure-control-group', css_class='rep'),  # Class rep tells it is replicable item
                        Field('image', wrapper_class='norep pure-control-group', css_class='rep'),  # Class norep tells the item must be removed from replica's
                        Field('content', wrapper_class='rep pure-control-group', css_class='rep'),
                        Hidden('id', section.id),
                        css_class='section',
                        css_id='sec',
                        data_section_id=1,
                        data_article_id=section.article_id
                    )
                )
            else:
                delim = '_' + str(section.section_order)
                secnum = section.section_order
                layouts.append(
                    Div(
                        Field('title' + delim, wrapper_class='rep pure-control-group', css_class='rep'),  # Class rep tells it is replicable item
                        Field('score' + delim, wrapper_class='rep pure-control-group', css_class='rep'),  # Class rep tells it is replicable item
                        Field('content' + delim, wrapper_class='rep pure-control-group', css_class='rep'),
                        Hidden('id' + delim, section.id),
                        css_class='section',
                        css_id='sec' + delim,
                        data_section_id=secnum
                    )
                )

        layouts.append(Field('tags', wrapper_class='norep pure-control-group', css_class='norep'))
        layouts.append(ButtonHolder(
            Hidden('article', artcle_id),
            Submit('submit', 'Update Post', css_id='submit', css_class='pure-button pure-button-primary'),
            css_id='buttons'
        ))

        self.helper.layout = Layout(
            *layouts
        )

    class Media:
        js = (
        )
