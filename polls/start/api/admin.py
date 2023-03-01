from django.contrib import admin
from services.models import Choice, Question, VoteHistory, UserInfo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name_plural = 'UserInfo'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInfoInline,)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'status'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('id', 'question_text', 'pub_date', 'status', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice_text', 'votes')


class VoteHistoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(VoteHistory, VoteHistoryAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)