import random
from datetime import datetime
from django.utils import timezone
from common.constants import CURRENT_TIME
from services.models import Question, VoteHistory, Choice
from common.utils import objects_to_json


def create_question(body, user):
    question_created = Question.objects.create(
        question_text=body['question_text'],
        pub_date=CURRENT_TIME,
        expire_date=timezone.make_aware(datetime.strptime(body['expire_date'], '%Y-%m-%d %H:%M:%S')),
        status=True,
        user_created=user,
        type=body['type'],
        pass_code=random.randint(100000, 999999)
    )
    choices_list = body['choice']
    for choice in choices_list:
        question_created.choice_set.create(choice_text=choice, votes=0)
    return question_created.as_json()


def update_question(id, body):
    question_updated = Question.objects.filter(id=id)
    question = Question.objects.get(id=id)
    if "question_text" in body:
        question_updated.update(question_text=body['question_text'])
    if "expire_date" in body:
        question_updated.update(expire_date=timezone.make_aware(datetime.strptime(body['expire_date'], '%Y-%m-%d %H:%M:%S')))
    if "status" in body:
        question_updated.update(status=body['status'])
    if "type" in body:
        question_updated.update(type=body['type'])
    if "choice" in body:
        choices_list = body['choice']
        for choice in choices_list:
            Choice.objects.filter(question=question).update(choice_text=choice)
    return objects_to_json(question_updated)


def check_question_owner(user, id):
    question_check = Question.objects.get(id=id)
    if question_check.user_created == user:
        return True
    else:
        return False


def get_question_by_id(id):
    return Question.objects.get(id=id)


def get_choice_set_by_question_id(question, id):
    return question.choice_set.get(id=id)


def create_vote_history(question, user_voted, choice_text):
    result = VoteHistory.objects.create(
        question=question,
        user_voted=user_voted,
        choice_text=choice_text)
    return result.as_json()


def get_active_public_question():
    results = Question.objects.filter(status=True, type=1).order_by('pub_date')
    return objects_to_json(results)


def search_question_by_text(query):
    results = Question.objects.filter(question_text__icontains=query)
    return objects_to_json(results)


def get_vote_info(question):
    results = VoteHistory.objects.filter(question=question)
    return objects_to_json(results)


def get_question_by_user(user):
    results = Question.objects.filter(user_created=user).order_by('pub_date')
    return objects_to_json(results)


def get_vote_history_by_user(user):
    results = VoteHistory.objects.filter(user_voted=user)
    return objects_to_json(results)