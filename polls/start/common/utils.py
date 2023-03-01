from django import http
from .constants import *
import json
from datetime import date as date_type, time as time_type
from django.db.models.fields.files import FieldFile


def dict_to_json(data, fields=None, exclude=None, **kwargs):
    """
    Return a JSON-dumpable dict
    """
    for attr in data:
        if isinstance(data[attr], time_type):
            data[attr] = data[attr].strftime(kwargs.get('time_format', '%H:%M:%S'))
        elif isinstance(data[attr], date_type):
            data[attr] = data[attr].strftime(kwargs.get('date_format', '%Y-%m-%d %H:%M:%S'))
        elif isinstance(data[attr], FieldFile):
            file_data = {}
            for k in kwargs.get('file_attributes', ('url',)):
                file_data[k] = data[attr].__getattribute__(k) if hasattr(data[attr], k) else ''
            data[attr] = file_data
    return data


def to_json(data, ensure_ascii=False, ensure_bytes=False, default=None):
    """
    Use in api_response_data
    Return data in Json
    """
    result = json.dumps(data, ensure_ascii=ensure_ascii, separators=(',', ':'), default=default)
    if ensure_bytes and isinstance(result, str):
        result = result.encode('utf-8')
    return result


def api_response_data(data, status=FAIL):
    """
    Use in api app to return response
    """
    if status == SUCCESSFUL:
        data = {
            'status': SUCCESSFUL,
            'payload': data
        }
    else:
        data['status'] = FAIL
    return http.HttpResponse(to_json(data), content_type='application/json; charset=utf-8')


def objects_to_json(objects):
    """
    Converts a Django QuerySet to a JSON string
    """
    objects_list = []
    for object in objects:
        object_json = object.as_json()
        objects_list.append(object_json)
    return objects_list







