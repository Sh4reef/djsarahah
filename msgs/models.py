from django.db import models
from django.utils.encoding import smart_text
from django_hosts.resolvers import reverse as host_reverse
from django.contrib.auth.models import User

# Create your models here.
from .validators import URLsNotAllowed

def set_deleted_user():
    return User.objects.get_or_create(username='deleted')

class MsgManager(models.Manager):
    def user_messages(self, user):
        user_obj = User.objects.get(username=user)
        query = Msg.objects.filter(user=user_obj).order_by('user')
        return query
    def sent_messages(self, user):
        user_obj = User.objects.get(username=user)
        query = Msg.objects.filter(sender=user_obj).order_by('sender')
        return query
    def favorite_messages(self, user):
        query = self.user_messages(user).filter(favorite=True)
        return query

class Msg(models.Model):
    user = models.ForeignKey(
        User,
        related_name='%(app_label)s_%(class)s_user_related',
        on_delete=models.CASCADE,
        default=1
    )
    message = models.TextField(max_length=240, validators=[URLsNotAllowed])
    sender = models.ForeignKey(
        User,
        related_name='%(app_label)s_%(class)s_sender_related',
        on_delete=models.SET(set_deleted_user),
        blank=True,
        null=True
    )
    favorite = models.BooleanField(default=False)
    objects = MsgManager()

    def __str__(self):
        return str(self.message)
    def get_absolute_url(self):
        return host_reverse('message', host='www', kwargs={'pk': self.pk})
