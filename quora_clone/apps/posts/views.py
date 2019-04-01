from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, FormView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Upvotes, Bookmarks, FollowQuestion, AnswerLater
from .forms import AnswerCreationForm, AnswerEditForm


class CreateAnswerView(CreateView):
    form_class = AnswerCreationForm
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        valid = super().form_valid(form)
        return valid


class UpdateAnswerView(UpdateView):
    form_class = AnswerEditForm
    success_url = reverse_lazy('home-page')


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


class FollowQuestionAjax(View):
    def post(self, request):
        if self.request.is_ajax():
            question_id = request.POST['question_id']
            user_id = request.POST['user_id']
            data = {}
            try:
                follow_question = FollowQuestion.objects.get_or_create(user_id=user_id, question_id=question_id)
                if follow_question[1]:
                    data['status'] = 'questionFollowed'
                else:
                    # Delete if was already bookmarked
                    follow_question[0].delete()
                    data['status'] = 'questionUnfollowed'
            except ObjectDoesNotExist as e:
                data['status'] = 'error'
            return JsonResponse(data)


class RemindQuestionAjax(View):
    def post(self, request):
        if self.request.is_ajax():
            question_id = request.POST['question_id']
            user_id = request.POST['user_id']
            data = {}
            try:
                follow_question = AnswerLater.objects.get_or_create(user_id=user_id, question_id=question_id)
                if follow_question[1]:
                    data['status'] = 'reminderCreated'
                else:
                    # Delete if was already bookmarked
                    follow_question[0].delete()
                    data['status'] = 'reminderDeleted'
            except ObjectDoesNotExist as e:
                data['status'] = 'error'
            return JsonResponse(data)
