from django import template
from django.template.loader import get_template
from django.template.context import Context
from django.conf import settings


register = template.Library()


class MetaDataNode(template.Node):
    def __init__(self, description="", keywords=""):
        self.description = description and description or settings.DEFAULT_META_DATA['description']
        self.keywords = keywords and keywords or settings.DEFAULT_META_DATA['keywords']

    def render(self, context):
        t = get_template("metadata.html")
        context['meta_description'] = self.description
        context['meta_keywords'] = self.keywords
        t.render(Context(context))

def do_get_metadata_from_obj(parser, tokens):
    """
    {% get_metadata_from_obj object description keyword %}

    object (object): Object to lookup
    description (str): Field name for description
    keyword (str): Field name for keyword

    """
    bits = list(tokens.split_contents())
    args = bits[1:]
    arg_names = ('description', 'keywords')
    def_arg_attrs = ('title', 'tags.names')
    arg_values = {name: "" for name in arg_names}
    other_args = args[1:]

    if len(args) < 1 or len(args) > 3:
        raise template.TemplateSyntaxError("Template tag should be in "
                                           "format {% get_metadata_from_obj object %} at the least")

    lookup_object = args[0]

    other_args = other_args if other_args else def_arg_attrs

    for count in range(len(other_args)):
        arg_values[arg_names[count]] = getattr(lookup_object, other_args[count], "")

    arg_values['lookup_object'] = lookup_object
    return MetaDataNode(**arg_values)


def do_get_metadata_from_str(parser, tokens):
    bits = list(tokens.split_contents())
    args = bits[1:]
    # if not len(args) == 2:
    #     raise template.TemplateSyntaxError("Template tag should be in "
    #                                        "format {% get_metadata_from_str description keywords %} at the least")

    return MetaDataNode(*args)


register.tag('get_metadata_from_obj', do_get_metadata_from_obj)
register.tag('get_metadata_from_str', do_get_metadata_from_str)
