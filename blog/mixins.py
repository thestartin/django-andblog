from django.http import JsonResponse

__all__ = ['JSONResponseMixin']


class JSONResponseMixin(object):
    response_json = {
        'status': 'SUCCESS',
        'message': ''
    }

    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        return self.response_json