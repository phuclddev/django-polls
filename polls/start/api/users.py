from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from common.utils import api_response_data
from common import constants
from common.constants import *
from services.users import user_manager
from services.questions import question_manager
from django.views.decorators.csrf import csrf_exempt
from .schema import *
from common.decorator import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from common.logger import log


@require_http_methods(["GET"])
def test(request):
# Test Logging lib
    log.error('This is log error')
    log.info('This is log info')
    log.exception('this is log exception')
    log.warning('This is log warning')
    log.data('This is log data')
    log.fatal('This is log fatal')
    return api_response_data({
        "user": {
            "id": 3,
            "last_login": "2023-02-22 01:38:39",
            "username": "user2",
            "first_name": "",
            "last_name": "",
            "email": "",
            "is_staff": "false",
            "is_active": "true",
            "date_joined": "2023-02-20 08:59:53",
            "type": 2
        }
    }, SUCCESSFUL)
    # return api_response_data({
    #     "error": "error_not_logged_in"
    # })


# Content-Type: application/x-www-form-urlencoded
@csrf_exempt
@require_http_methods(["POST"])
def my_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user_name = user.get_username()
        user_infos = user_manager.get_infos_json(user_name)
        return api_response_data({
        "user": user_infos,
    }, SUCCESSFUL)
    else:
        return api_response_data({
        "error": constants.ErrorCode.ERROR_INVALID_CREDENTIALS,
    })


def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@my_login_required
@require_http_methods(["GET"])
def get(request):
    user = request.user
    user_name = user.get_username()
    user_infos = user_manager.get_infos_json(user_name)
    question = question_manager.get_question_by_user(user)
    vote_history = question_manager.get_vote_history_by_user(user)
    return api_response_data({
        "user": user_infos,
        "question": question,
        "vote_history": vote_history,
    }, SUCCESSFUL)


@csrf_exempt
@my_login_required
@require_http_methods(["POST"])
@parse_params(question_create_schema)
def create_question(request, body):
    user_name = request.user.get_username()
    user = User.objects.get(username=user_name)
    if user_manager.check_user_type(user):
        question_created = question_manager.create_question(body, user)
        return api_response_data({
            "question_created": question_created,
        }, SUCCESSFUL)
    else:
        return api_response_data({
            "error_code": constants.ErrorCode.ERROR_BASIC_ACCOUNT,
        })


@csrf_exempt
@my_login_required
@require_http_methods(["PUT"])
@parse_params(question_update_schema)
def update_question(request, body, id):
    if question_manager.check_question_owner(request.user, id):
        question_updated = question_manager.update_question(id, body)
        return api_response_data({
            "question_updated": question_updated,
        }, SUCCESSFUL)
    else: api_response_data({
            "error_code": constants.ErrorCode.ERROR_BASIC_ACCOUNT,
        })


@csrf_exempt
@my_login_required
@require_http_methods(["POST"])
@parse_params(vote_schema)
def vote(request, body):
    question = question_manager.get_question_by_id(body['question_id'])
    selected_choice = question_manager.get_choice_set_by_question_id(question, body['choice_id'])
    vote_created_info = question_manager.create_vote_history(question, request.user, selected_choice.choice_text)
    return api_response_data({
        "vote_created_info": vote_created_info,
    }, SUCCESSFUL)
