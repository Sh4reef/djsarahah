from django.conf import settings
from django_hosts import patterns, host

from django_edition.hostsconfig.views import viewing_user

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'admin', 'django_edition.urls.admin', name='admin'),
    host(r'(?P<username>\w+)', 'django_edition.urls.user', callback=viewing_user, name='user'),
    # host(r'(\w+)', 'django_edition.hostsconfig.urls', name='wildcard'),
)
