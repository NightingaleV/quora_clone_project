"""quora_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from quora_clone.apps.posts.views import ListUnansweredQuestion, FeedAnsweredQuestions

urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/index.html'), name='home-page'),
    path('answered-questions/', FeedAnsweredQuestions.as_view(), name='answered-questions-list'),
    path('unanswered-questions/', ListUnansweredQuestion.as_view(), name='unanswered-questions-list'),
    path('topics/', include('quora_clone.apps.topics.urls')),
    path('users/', include('quora_clone.apps.users.urls')),
    path('actions/', include('quora_clone.apps.posts.ajax_urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
