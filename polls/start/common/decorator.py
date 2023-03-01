from jsonschema import Draft202012Validator
import json
from functools import wraps
from django.views import defaults
from .utils import api_response_data
from .constants import *

def response_http_404(request):
    return defaults.page_not_found(request, '')


def parse_params(schema, error_handler=response_http_404):
    def _parse_params(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            body = json.loads(request.body.decode("utf-8"))
            draft_202012_validator = Draft202012Validator(schema)
            if draft_202012_validator.is_valid(body):
                return func(request, body, *args, **kwargs)
            else:
                return error_handler(request)
        return wrapper
    return _parse_params


def my_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return api_response_data({'status': FAIL, 'payload': {'error_code': ErrorCode.ERROR_NOT_LOGGED_IN}})
        else:
            return func(request, *args, **kwargs)
    return wrapper


