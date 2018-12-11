from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, FormView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserCreationForm

User = get_user_model()


class UserCreateView(FormView):
    form_class = UserCreationForm
    template_name = 'users/users_register.html'
    success_url = reverse_lazy('home-page')


class UserLoginView(LoginView):
    template_name = 'users/users_login.html'


class UserRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('home-page')
