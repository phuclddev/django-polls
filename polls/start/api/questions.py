from django.views.decorators.http import require_http_methods
from services.questions import question_manager
from common.utils import api_response_data
from common.constants import *
from common.decorator import *
from asgiref.sync import sync_to_async


@lock((lambda request: request.user.id), 'lock_user_get',
    locked_handler=(lambda *args: response_too_many_requests(args)))
# @sync_to_async
@require_http_methods(["GET"])
def get(request):
    question_active_public = question_manager.get_active_public_question()
    return api_response_data({
        "question_active_public": question_active_public,
    }, SUCCESSFUL)


@require_http_methods(["GET"])
def search(request):
    query = request.GET.get("question_text")
    search_results = question_manager.search_question_by_text(query)
    return api_response_data({
        "search_results": search_results,
    }, SUCCESSFUL)
