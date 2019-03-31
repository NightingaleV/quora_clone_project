from django.urls import path
from .views import UpvoteAnswerAjax, BookmarkAnswerAjax, FollowQuestionAjax, RemindQuestionAjax

app_name = 'posts_ajax'

urlpatterns = [
    path('upvote-answer/', UpvoteAnswerAjax.as_view(), name='upvote-answer'),
    path('bookmark-answer/', BookmarkAnswerAjax.as_view(), name='bookmark-answer'),
    path('follow-question/', FollowQuestionAjax.as_view(), name='follow-question'),
    path('remind-question/', RemindQuestionAjax.as_view(), name='remind-question'),
]

