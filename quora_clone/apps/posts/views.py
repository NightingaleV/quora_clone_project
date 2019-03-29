from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from .models import Upvotes, Bookmarks


# Create your views here.
class UpvoteAnswerAjax(View):
    def post(self, request):
        # self.request == request -> request is an attribute and also a parameter, but why... hm ?
        if self.request.is_ajax():
            answer_id = request.POST['answer_id']
            user_id = request.POST['user_id']
            data = {}
            try:
                upvote = Upvotes.objects.get_or_create(answer_id=answer_id, user_id=user_id)
                # Means answer wasn't upvoted before
                if upvote[1]:
                    data['status'] = 'upvoteSaved'
                else:
                    # Delete if was already upvoted
                    upvote[0].delete()
                    data['status'] = 'upvoteDeleted'
            except ObjectDoesNotExist as e:
                data['status'] = 'error'
            return JsonResponse(data)


class BookmarkAnswerAjax(View):
    def post(self, request):
        # self.request == request, they are attributes and also parameters
        if self.request.is_ajax():
            answer_id = request.POST['answer_id']
            user_id = request.POST['user_id']
            data = {}
            try:
                bookmark = Bookmarks.objects.get_or_create(bookmark_id=answer_id, user_id=user_id)
                # Means answer wasn't bookmarked before
                if bookmark[1]:
                    data['status'] = 'bookmarkSaved'
                else:
                    # Delete if was already bookmarked
                    bookmark[0].delete()
                    data['status'] = 'bookmarkDeleted'
            except ObjectDoesNotExist as e:
                data['status'] = 'error'
            return JsonResponse(data)
