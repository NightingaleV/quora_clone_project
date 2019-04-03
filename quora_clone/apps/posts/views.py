from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, FormView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Question, Answer, Upvotes, Bookmarks, FollowQuestion, AnswerLater
from .forms import AnswerCreationForm, AnswerEditForm


class CreateAnswerView(CreateView):
    form_class = AnswerCreationForm
    template_name = 'posts/_modal_answer_create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateAnswerView, self).get_context_data()
        if self.request.method == 'GET':
            context['modal_question'] = Question.objects.get(id=self.request.GET.get('question_id'))
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        if self.request.is_ajax():
            self.object.save()
            data = {'status': 'success'}
            return JsonResponse(data)
        valid = super().form_valid(form)
        return valid


class EditAnswerView(UpdateView):
    model = Answer
    form_class = AnswerEditForm
    # success_url = reverse_lazy('home-page')
    template_name = 'posts/_modal_answer_edit.html'
    pk_url_kwarg = 'answer_id'

    def form_valid(self, form):
        if self.request.is_ajax():
            self.object = form.save()
            data = {'status': 'success'}
            return JsonResponse(data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EditAnswerView, self).get_context_data()
        context['modal_question'] = Question.objects.get(pk=self.object.question.pk)
        return context


# Create your views here.
class DeleteAnswerAjax(View):
    def post(self, request):
        if self.request.is_ajax():
            answer_id = request.POST['answer_id']
            user_id = self.request.user.pk
            data = {}
            try:
                answer = Answer.objects.get(id=answer_id, user_id=user_id)
                answer.delete()
                data['status'] = 'answerDeleted'
            except ObjectDoesNotExist as e:
                data['status'] = 'error'

            return JsonResponse(data)


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
