from django.urls import path
from api import users, questions, results

app_name = 'api'
urlpatterns = [
    # mock Test API for front-end
    path('user/get/test', users.test),
    #
    path('auth/login/', users.my_login),
    path('auth/logout/', users.my_logout),
    path('user/get/', users.get),
    path('user/createQuestion/', users.create_question),
    path('user/createQuestion/<int:id>/', users.update_question),
    path('user/vote/', users.vote),
    path('question/get/', questions.get),
    path('question/search/', questions.search),
    path('<int:id>/result/', results.get)
]