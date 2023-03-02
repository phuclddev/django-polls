from jsonschema import Draft202012Validator
import json
from functools import wraps
from django.views import defaults
from .utils import api_response_data
from .constants import *
from asgiref.sync import sync_to_async
import time
import sys
from common.logger import log
from django import http
import asyncio
from django.core.cache import cache
from django.conf import settings
import collections


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


def get_request_ip(request):
    return request.META['REMOTE_ADDR']


async def _call_request_user(request):
    try:
        request.user.as_dict
    except:
        await sync_to_async(bool)(request.user)


def log_request(log_response=True, max_response_length=500, log_request_body=True, max_request_body_length=100):
    def _log_request(func):
        @wraps(func)
        async def _func(request, *args, **kwargs):
            await _call_request_user(request)
            start = time.time()
            ex = None
            try:
                if asyncio.iscoroutinefunction(func):
                    response = await func(request, *args, **kwargs)
                else:
                    response = func(request, *args, **kwargs)
            except Exception as excep:
                ex = excep
                ex_type, ex_value, ex_traceback = sys.exc_info()
                log.exception('%s_exception', func.__name__)
            end = time.time()
            elapsed = int((end - start) * 1000)
            if log_request_body:
                if hasattr(request, '_body'):
                    request_body = request.body
                elif request.POST:
                    request_body = 'POST:' + to_json(request.POST, ensure_bytes=True)
                    if request.FILES:
                        files_info = dict([(k, {v.name: v.size}) for k, v in request.FILES.items()])
                        request_body += ';FILES:' + to_json(files_info, ensure_bytes=True)
                else:
                    request_body = ''
                if max_request_body_length and len(request_body) > max_request_body_length:
                    request_body = str(request_body[:max_request_body_length]) + '...'
            else:
                request_body = ''
            if ex is None:
                status_code = response.status_code
                if log_response:
                    if (status_code == 301 or status_code == 302) and 'Location' in response:
                        response_body = response['Location']
                    else:
                        response_body = response.content.decode("utf-8")
                        if max_response_length and len(response_body) > max_response_length:
                            response_body = response_body[:max_response_length] + '...'
                else:
                    response_body = ''
            else:
                if ex is http.Http404:
                    status_code = 404
                else:
                    status_code = 500
                response_body = 'exception:%s' % ex
            log.data('http_request|ip=%s,elapsed=%d,method=%s,url=%s,body=%s,status_code=%d,response=%s',
                get_request_ip(request), elapsed, request.method, request.get_full_path(),
                request_body, status_code, response_body)
            if ex is not None:
                raise ex_type
            return response

        return _func

    return _log_request

def geo_ip_to_country(ip):
    try:
        from django.contrib.gis.geoip import GeoIP
        if isinstance(ip, int):
            return GeoIP().country(convert.int_to_ip(ip))['country_code'] or 'ZZ'
        else:
            return GeoIP().country(ip)['country_code'] or 'ZZ'
    except:
        log.exception('geo_ip_to_country_exception')
        return 'ZZ'

_function_queue = []


class AcquireLockError(Exception):
    pass


def to_json(data, ensure_ascii=False, ensure_bytes=False, default=None):
	result = json.dumps(data, ensure_ascii=ensure_ascii, separators=(',', ':'), default=default)
	if ensure_bytes and isinstance(result, str):
		result = result.encode('utf-8')
	return result


def api_response(request, data):
    response = http.HttpResponse(to_json(data), content_type='application/json; charset=utf-8')
    return response


def response_too_many_requests(*args, **kwargs):
    request = args[0]
    return api_response(request, {
        'status': FAIL,
        'payload': {
            'error_code': 'too_many_requests'
        }
    })


def lock(fkey, group=None, **kwargs):
    """
    Decorator for locking a function with a fkey.

    :param fkey: the key for the lock. No function with the same key can run simultaneously.
        fkey can also be a function. All arguments of target function will be passed to it.
    :param group: the locking group. The functions with same key and different group can run simultaneously.
        Default is {settings.KEY_PREFIX}:{core}:{default_lock}
    :**kwargs:
        locked_handler: the function will be called instead of raising AcquireLockError when the lock can't be acquired.
            All arguments of target function will be passed to it.
    :returns: the return value of target function
    :raises AcquireLockError: can't acquire lock

    * Examples:
    @lock('pot')
    def inc_pot(pot):
        pot.value += 1
        pot.save()

    @lock((lambda request: request.user.uid), keys.PURCHASE, locked_handler=(lambda *args: response_json({'error': 'locked'}, 403)))
    def purchase(request):
        user = request.user
        if user.balance > 1000:
            user.balance -= 1000
            user.save()
            send_item(user)
        else:
            return response_json({'error': 'insufficient_fund'}, 403)
    """

    group = group or '{0}:{1}:{2}'.format(settings.KEY_PREFIX, 'core', 'default_lock')
    handler = kwargs.get('locked_handler')

    def _lock_decorator(func):
        def acquire_lock(key):
            if cache.get(key) is None:
                # The key doesn't exist, so set it with the given timeout
                cache.set(key, 1, timeout=settings.LOCK_TTL)
                return True
            else:
                # The key already exists, so we couldn't acquire the lock
                return False

        def release_lock(key):
            # log.debug('release lock {}'.format(key))
            return cache.delete(key)

        def _func_wrapper(*args, **kwargs):
            key = fkey(*args, **kwargs) if isinstance(fkey, collections.Callable) else fkey
            group_key = '{}_{}'.format(group, key)
            if acquire_lock(group_key):
                try:
                    if asyncio.iscoroutinefunction(func):
                        result = func(*args, **kwargs)
                    else:
                        result = func(*args, **kwargs)
                    return result
                finally:
                    release_lock(group_key)
            else:
                if handler is None:
                    raise AcquireLockError('Unable to acquire lock {}'.format(group_key))
                else:
                    return handler(*args, **kwargs)

        return _func_wrapper

    return _lock_decorator
