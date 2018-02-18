from django.conf.urls import url
from django.contrib import admin

from django_edition.hostsconfig.views import www_root_redirect

urlpatterns = [
    url(r'^$', www_root_redirect),
    url(r'^(?i)panel/', admin.site.urls),
]
