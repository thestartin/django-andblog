from django.http import HttpResponseBadRequest


class MultiFormMixin(object):
    """
    Mixin to use/process multiple forms in a view
    """
    def get_form_class(self, form_name=None):
        if not self.form_classes:
            # If there are no form classes return bad request.
            return HttpResponseBadRequest()

        if form_name:
            form = self.form_classes.get(form_name)
            if not form:
                return HttpResponseBadRequest()

            return form

        return tuple(self.form_classes.itervalues())

    def get_form(self, form_classes, form_name=None):
        if isinstance(form_classes, tuple):
            forms = []
            for form_class in form_classes:
                forms.append(form_class(**self.get_form_kwargs()))

            return forms
        else:
            return form_classes(**self.get_form_kwargs())
