from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import transaction
from django_hosts.resolvers import reverse as reverse_host

# Create your models here.

class Manage(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications = models.BooleanField(default=0)
    appear_in_search = models.BooleanField(default=1)
    allow_anonymous_user = models.BooleanField(default=1)
    user_absolute_url = models.URLField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self):
        return reverse_host('sub_send_message', host='user', host_kwargs={'username': self.username}, scheme='http')

def post_save_user_model_reciever(sender, instance, created, *args, **kwargs):
    if created:
        obj = Manage.objects.create(username=instance)
        obj.user_absolute_url = obj.get_absolute_url()
        obj.save()
post_save.connect(post_save_user_model_reciever, sender=User)
