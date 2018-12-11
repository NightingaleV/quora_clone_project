from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, FormView

from .forms import UserCreationForm

User = get_user_model()


class UserCreateView(FormView):
    form_class = UserCreationForm
    template_name = 'users/users_register.html'
    success_url = reverse_lazy('home-page')
