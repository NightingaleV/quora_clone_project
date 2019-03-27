from django.urls import path
from .views import UpvoteAnswerAjax, BookmarkAnswerAjax

app_name = 'posts'

urlpatterns = [
    path('upvote-answer', UpvoteAnswerAjax.as_view(), name='upvote-answer'),
    path('bookmark-answer', BookmarkAnswerAjax.as_view(), name='bookmark-answer'),
]
