from django.contrib import admin
from .models import Question, Answer


# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


# Register your models here.
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
