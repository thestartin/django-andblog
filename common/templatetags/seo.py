from django import template
from django.template.loader import get_template
from django.template.context import Context
from django.conf import settings
from django.db.models.query import ValuesListQuerySet
from django.contrib.sites.models import get_current_site


register = template.Library()


class MetaDataNode(template.Node):
    def __init__(self, description="", keywords="", page_title="", og_type="", site_url=""):
        self.description = description and description or '"{}"'.format(settings.DEFAULT_META_DATA['description'])
        self.keywords = keywords and keywords or '"{}"'.format(settings.DEFAULT_META_DATA['keywords'])
        self.page_title = page_title and page_title or self.description
        self.og_type = og_type and og_type or '"{}"'.format(settings.DEFAULT_META_DATA['og_type'])
        self.site_url = site_url and site_url or '"{}"'.format(''.join(['http://', get_current_site(None).domain]))

        # If variable was passed then resolve it that way
        self.metas = {'meta_description': self.description,
                      'meta_keywords': self.keywords,
                      'page_title': self.page_title,
                      'og_type': self.og_type,
                      'site_url': self.site_url}

        for meta in self.metas:
            self.metas[meta] = self.metas[meta][1:-1] if \
                (self.metas[meta][-1] == self.metas[meta][0] and self.metas[meta][0] in ('"', "'")) else \
                template.Variable(self.metas[meta])

        # self.description = self.description[1:-1] if \
        #     (self.description[-1] == self.description[0] and self.description[0] in ('"', "'")) else \
        #     template.Variable(self.description)
        #
        # self.keywords = self.keywords[1:-1] if \
        #     (self.keywords[-1] == self.keywords[0] and self.keywords[0] in ('"', "'")) else \
        #     template.Variable(self.keywords)
        #
        # self.page_title = self.page_title[1:-1] if \
        #     (self.page_title[-1] == self.page_title[0] and self.page_title[0] in ('"', "'")) else \
        #     template.Variable(self.page_title)
        #
        # self.og_type = self.og_type[1:-1] if \
        #     (self.og_type[-1] == self.og_type[0] and self.og_type[0] in ('"', "'")) else \
        #     template.Variable(self.og_type)

    def render(self, context):
        t = get_template("metadata.html")
        for meta in self.metas:
            self.metas[meta] = self.metas[meta].resolve(context) if \
                isinstance(self.metas[meta], template.Variable) else self.metas[meta]

            if meta == 'meta_keywords':
                if isinstance(self.metas[meta], (list, tuple, ValuesListQuerySet)):
                    self.metas[meta] = ','.join(self.metas[meta])

        # self.description = self.description.resolve(context) if \
        #     isinstance(self.description, template.Variable) else self.description
        # self.page_title = self.page_title.resolve(context) if \
        #     isinstance(self.page_title, template.Variable) else self.page_title
        # self.og_type = self.og_type.resolve(context) if \
        #     isinstance(self.og_type, template.Variable) else self.og_type
        # self.keywords = self.keywords.resolve(context) if \
        #     isinstance(self.keywords, template.Variable) else self.keywords
        #
        # if isinstance(self.keywords, (list, tuple, ValuesListQuerySet)):
        #     self.keywords = ','.join(self.keywords)

        # context['meta_description'] = self.description
        # context['meta_keywords'] = self.keywords
        # context['page_title'] = self.page_title
        # context['og_type'] = self.og_type
        return t.render(Context(self.metas))


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
    args = [item.replace('""', '') for item in bits[1:]]

    # if not len(args) == 2:
    #     raise template.TemplateSyntaxError("Template tag should be in "
    #                                        "format {% get_metadata_from_str description keywords %} at the least")

    return MetaDataNode(*args)


register.tag('get_metadata_from_obj', do_get_metadata_from_obj)
register.tag('get_metadata_from_str', do_get_metadata_from_str)
