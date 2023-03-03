from django.views.decorators.http import require_http_methods
from services.questions import question_manager
from common.utils import api_response_data
from common.constants import *


@require_http_methods(["GET"])
def get(request, id):
    question = question_manager.get_question_by_id(id)
    vote_result = question_manager.get_vote_info(question)
    return api_response_data({
        "question_result": question.as_json(),
        "vote_result": vote_result
    }, SUCCESSFUL)