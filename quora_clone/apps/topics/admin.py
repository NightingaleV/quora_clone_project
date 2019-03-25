from django.contrib import admin
from .models import Topic, TopicSubscription
from quora_clone.apps.posts.models import Question


class QuestionAdmin(admin.StackedInline):
    model = Question


class TopicSubscriptionInline(admin.TabularInline):
    model = TopicSubscription


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    inlines = [QuestionAdmin, TopicSubscriptionInline]
