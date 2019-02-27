from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, FormView
from django.contrib.auth import get_user
# Custom Imports
from .forms import UserCreationForm

User = get_user_model()


class UserCreateView(FormView):
    form_class = UserCreationForm
    template_name = 'users/users_register.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        form.save()
        valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = authenticate(username=username, password=password)
        login(self.request, user)
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


class UserPasswordResetCompleteView(PasswordResetCompleteView):\
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


class UserAccountView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/users_account.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserAccountView, self).get_context_data(**kwargs)
        return context


class UserProfileView(DetailView):
    template_name = 'users/users_profile.html'
    model = User
    slug_field = 'username'
    slug_url_kwarg = "username"
    context_object_name = 'user'
