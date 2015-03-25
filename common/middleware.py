from django.http import HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.template import loader


class HttpBadReponseMiddleware(object):
    def process_response(self, request, response):
        if isinstance(response, (HttpResponseForbidden, Http404, HttpResponseBadRequest)):
            context = RequestContext(request)
            template = "{}.html".format(response.status_code)
            response.content = loader.render_to_string(template, context_instance=context)
        return response
