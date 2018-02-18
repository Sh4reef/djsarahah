from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from allauth.account.forms import ChangePasswordForm

# Create your views here.

from .forms import ManageForm
from .models import Manage

class ManageView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = 'users/manage_form.html'
    form_class = ManageForm
    login_url = '/account/login/'
    success_url = '/manage/'
    success_message = 'Your profile has been successfully updated.'
    def get_context_data(self, *args, **kwargs):
        context = super(ManageView, self).get_context_data(*args, **kwargs)
        context['change_password_form'] = ChangePasswordForm
        return context
    def get_queryset(self):
        logged_user = self.request.user
        self.queryset = get_object_or_404(User, username=logged_user)
        return self.queryset
    def get_initial(self):
        user_obj = self.get_queryset()
        initial = {
            'name': user_obj.first_name,
            'email': user_obj.email,
            'notifications': user_obj.manage.notifications,
            'appear_in_search': user_obj.manage.appear_in_search,
            'allow_anonymous_user': user_obj.manage.allow_anonymous_user,
        }
        return initial
    def form_valid(self, form):
        user_obj = self.get_queryset()
        user_obj.first_name = form.cleaned_data.get('name')
        user_obj.email = form.cleaned_data.get('email')
        user_obj.manage.notifications = form.cleaned_data.get('notifications')
        user_obj.manage.appear_in_search = form.cleaned_data.get('appear_in_search')
        user_obj.manage.allow_anonymous_user = form.cleaned_data.get('allow_anonymous_user')
        user_obj.save()
        user_obj.manage.save()
        return super(ManageView, self).form_valid(form)
    def post(self, request, *args, **kwargs):
        if request.POST.get('manage'):
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            return self.form_invalid(form)
        if request.POST.get('remove'):
            user_obj = self.get_queryset()
            user_obj.delete()
            success_url = '/'
            messages.error(request, 'Account deleted.')
            return HttpResponseRedirect(success_url)
