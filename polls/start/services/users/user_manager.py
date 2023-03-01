from django.contrib.auth.models import User
from services.models import UserInfo, Question
from common.utils import dict_to_json
from django.utils import timezone


def get_infos_json(user_name):
    """
    From Username then Return User info as Json
    """
    if not user_name:
        return {}
    user = User.objects.get(username=user_name)
    user_info = UserInfo.objects.get(user=user)
    user = user.__dict__
    user.pop('_state', None)
    user.pop('password', None)
    user.pop('is_superuser', None)
    user["type"] = user_info.type
    user_json = dict_to_json(user)
    return user_json


def check_user_type(user):
    today = timezone.now().date()
    user_info = UserInfo.objects.get(user=user)
    question = Question.objects.filter(pub_date__date=today, user_created=user)
    if user_info.check_type():
        return True
    else:
        if question is None:
            return True
        else:
            return False