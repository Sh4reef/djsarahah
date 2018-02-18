from django.conf.urls import url, include


from msgs.views import SendMessage



urlpatterns = [
    url(r'^$', SendMessage.as_view(), name='sub_send_message'),
    url(r'^', include('django_edition.urls.global')),
    url(r'^(?i)account/', include('allauth.urls')),
]
