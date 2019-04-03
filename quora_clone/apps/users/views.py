from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from django.views.generic import DetailView, View, ListView, RedirectView, UpdateView, CreateView, FormView
from django.contrib.auth import get_user
# For aggregation
from django.db.models import Count, Sum
from quora_clone.apps.posts.models import Answer
# Custom Imports
from .forms import UserCreationForm, UserUpdateForm
from .models import UserFollowersBridge
User = get_user_model()


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/users_register.html'

    # success_url = reverse_lazy('home-page')

    def get_success_url(self):
        url = reverse_lazy('users:profile', kwargs={'alias': self.request.user.username})
        return url

    def form_valid(self, form):
        self.object = form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class UserUpdateView(UpdateView):
    template_name = 'users/users_profile_edit.html'
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        valid = super().form_valid(form)

        return valid


class UserLoginView(LoginView):
    template_name = 'users/users_login.html'


class UserLogoutView(LogoutView):
    next_page = 'users:login'


# PASSWORD RESET
class UserPasswordResetView(PasswordResetView):
    template_name = 'users/users_password_reset.html'
    success_url = reverse_lazy('users:password-reset-done')
    html_email_template_name = 'users/users_password_reset_email.html'
    email_template_name = 'users/users_password_reset_email.html'


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/users_password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/users_password_reset_confirm.html'
    success_url = reverse_lazy('users:password-reset-complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView): \
        template_name = 'users/users_password_reset_complete.html'


# PASSWORD CHANGE
class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/users_password_change.html'
    success_url = reverse_lazy('users:password-change-done')


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'users/users_password_change_done.html'


class UserRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('home-page')


class UserProfileView(DetailView):
    template_name = 'users/users_profile.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = "alias"
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statistics'] = Answer.data.filter(user=self.object.pk).add_upvote_counter().aggregate(Sum('num_upvotes'))
        context['num_answers'] = Answer.data.filter(user=self.object.pk).count()
        context['user_followers'] = UserFollowersBridge.objects.filter(following=self.object.pk).count()
        return context


class UserFollowAjax(View):
    def post(self, request):
        # self.request == request, they are attributes and also parameters
        if self.request.is_ajax():
            follower_id = request.POST['follower_id']
            following_id = request.POST['following_id']
            data = {}
            try:
                follow = User.objects.get_or_create(follower_id=follower_id, following_id=following_id)
                # Means user wasn't followed before
                if follow[1]:
                    data['status'] = 'followingCreated'
                else:
                    # Delete if was already followed
                    follow[0].delete()
                    data['status'] = 'followingDeleted'
            except ObjectDoesNotExist as e:
                data['status'] = 'objectDoesNotExist'
            return JsonResponse(data)
