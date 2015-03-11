from django.http import JsonResponse

__all__ = ['JSONResponseMixin']


class JSONResponseMixin(object):
    failure_message = {'status': 'N', 'message': 'Unable to process request', 'data': ''}
    success_message = {'status': 'Y', 'message': 'Successfully processed request', 'data': ''}

    def render_to_json_response(self, context, **response_kwargs):

        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        return context
