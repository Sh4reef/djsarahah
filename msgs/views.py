from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, DetailView
from django_hosts.resolvers import reverse as host_reverse
from django.core.serializers import serialize
from django.http import JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger

# Create your views here.

from .models import Msg
# from .forms import MsgForm



class SendMessage(SuccessMessageMixin, CreateView):
    model = Msg
    fields = ['user', 'message', 'sender']
    success_url = '/'
    success_message = 'Message sent to {user}.'
    def get_success_message(self, *args, **kwargs):
        return self.success_message.format(user=self.object.user)
    def get_context_data(self, *args, **kwargs):
        context = super(SendMessage, self).get_context_data(*args, **kwargs)
        context['obj'] = get_object_or_404(User, username=self.request.viewing_user)
        return context
    def form_valid(self, form):
        user = self.request.viewing_user
        form.instance.user = user
        try:
            form.instance.sender = self.request.user
        except ValueError:
            form.instance.sender = None
        return super(SendMessage, self).form_valid(form)

class MessagesListView(LoginRequiredMixin, ListView):
    model = Msg
    paginate_by = 2
    login_url = '/account/login/'
    def get_queryset(self, type=None):
        if type == 'received':
            queryset = self.model.objects.user_messages(user=self.request.user)
        elif type == 'sent':
            queryset = self.model.objects.sent_messages(user=self.request.user)
        elif type == 'favorite':
            queryset = self.model.objects.favorite_messages(user=self.request.user)
        else:
            queryset = self.model.objects.all().order_by('message')
        return queryset
    def get_context_data(self, **kwargs):
        context = super(MessagesListView, self).get_context_data(**kwargs)
        user_messages = self.get_paginator(self.get_queryset(type='received'), self.paginate_by)
        sent_messages = self.get_paginator(self.get_queryset(type='sent'), self.paginate_by)
        favorite_messages = self.get_paginator(self.get_queryset(type='favorite'), self.paginate_by)
        context['user_messages'] = user_messages.page(int(1))
        context['sent_messages'] = sent_messages.page(int(1))
        context['favorite_messages'] = favorite_messages.page(int(1))
        return context
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if request.is_ajax():
            msg_type = request.GET.get('msg_type')
            page = request.GET.get(self.page_kwarg)
            query = self.get_paginator(self.get_queryset(type=msg_type), self.paginate_by)
            try:
                msgs = query.page(int(page))
            except PageNotAnInteger:
                msgs = query.page(1)
            except EmptyPage:
                msgs = query.page(query.num_pages)
            # msg_list = serialize('json', msgs, use_natural_foreign_keys=True, fields=['message'])
            msg_list = {}
            for msg in msgs.object_list:
                if msg.favorite:
                    toggle_icon = 'fa-heart text-danger fa'
                else:
                    toggle_icon = 'fa-heart-o text-secondary fa'
                msg_list[str(msg.id)] = {'message': str(msg.message), 'url': str(msg.get_absolute_url()), 'message_id': 'message_' + str(msg.id), 'toggle_icon': toggle_icon}
                # msg_list[str(msg.get_absolute_url())] = msg.get_absolute_url()
            data = {
                'msgs': msg_list,
                'hasNext': msgs.has_next(),
            }
            return JsonResponse(data, safe=False)
        return self.render_to_response(self.get_context_data())

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Msg
    def get(self, request, *args, **kwargs):
        obj_id = self.kwargs.get(self.pk_url_kwarg)
        self.object = self.model.objects.get(pk=obj_id)
        obj = self.object
        if request.is_ajax():
            favoriteToggle = request.GET.get('favoriteToggle')
            if favoriteToggle == 'OFF':
                obj.favorite = True
                obj.save()
                isFavorite = True
                toggle_icon = 'fa-heart text-danger fa'
            elif favoriteToggle == 'ON':
                obj.favorite = False
                obj.save()
                isFavorite = False
                toggle_icon = 'fa-heart-o text-secondary fa'
            else:
                return None
            data = {
                'isFavorite': isFavorite,
                'toggleIcon': toggle_icon,
                'message_id': 'message_{}'.format(obj.id),
                'url': obj.get_absolute_url(),
                'msg': obj.message,
            }
            return JsonResponse(data, safe=False)
        return self.render_to_response(self.get_context_data())
