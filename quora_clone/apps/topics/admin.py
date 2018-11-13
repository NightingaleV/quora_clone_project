from django.contrib import admin
from .models import Topic, TopicSubscription


class TopicSubscriptionInline(admin.TabularInline):
    model = TopicSubscription


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    inlines = [TopicSubscriptionInline]

