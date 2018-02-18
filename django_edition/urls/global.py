from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin

from allauth.account.views import PasswordChangeView

from msgs.views import MessagesListView, MessageDetailView
from users.views import ManageView

from django_edition.hostsconfig.views import search_view

urlpatterns = [
    url(r'^(?i)messages/$', MessagesListView.as_view(), name='messages'),
    url(r'^(?i)message/(?P<pk>\d+)$', MessageDetailView.as_view(), name='message'),
    url(r'^(?i)manage/$', ManageView.as_view(), name='manage'),
    url(r'^(?i)manage/changepassword/$', PasswordChangeView.as_view(), name='manage_passwword_change'),
    url(r'^(?i)search/$', search_view, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
