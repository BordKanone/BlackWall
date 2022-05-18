from django.http import JsonResponse
from rest_framework import status


class ProcessException:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        return JsonResponse(str(exception), safe=False, status=status.HTTP_402_PAYMENT_REQUIRED)
