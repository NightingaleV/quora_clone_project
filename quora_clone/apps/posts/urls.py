from django.urls import path
from .views import DetailQuestion

app_name = 'posts'

urlpatterns = [
    path('<slug:question_slug>/', DetailQuestion.as_view(), name='question-detail'),
]
