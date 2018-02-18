import re
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.contrib.auth.models import User
from django_hosts.resolvers import reverse as host_reverse
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse

from msgs.models import Msg
from users.models import Manage
from .forms import CheckUsernameForm

def home(request):
    form = CheckUsernameForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        request.session['available_username'] = username
        signup_url = host_reverse('account_signup', host='www')
        return redirect(signup_url)
    if request.is_ajax():
        if request.GET.get('check_username'):
            data = {}
            username = request.GET.get('check_username')
            myreg = re.compile('[a-zA-Z0-9]')
            sub_username = myreg.sub('', username)
            if sub_username.__len__() != 0:
                data.update({'status':0})
                return JsonResponse(data)
            try:
                User.objects.get(username__iexact=username)
                data.update({'status': 0})
            except:
                data.update({'status': 1})
            return JsonResponse(data)
    return render(request, 'home.html', {'form': form})

def viewing_user(request, username):
    home_redirect = host_reverse('home', host='www')
    full_url = home_redirect + request.get_full_path().strip('/')
    if request.get_host() == settings.PARENT_HOST:
        return redirect(full_url)
    try:
        request.viewing_user = get_object_or_404(User, username__iexact=username)
    except:
        raise Http404()

def search_view(request):
    if request.is_ajax():
        if request.method == 'GET':
            query = request.GET.get('q')
            if query:
                objs = Manage.objects.filter(
                    Q(username__username__icontains=query)|
                    Q(username__first_name__icontains=query),
                    appear_in_search=True
                )
                user = serialize(
                    'json',
                    objs,
                    use_natural_foreign_keys=True,
                    fields=['username', 'user_absolute_url']
                )
            return JsonResponse(user, safe=False)
        return response
    if request.GET.get('q'):
        query = request.GET.get('q')
        if query:
            objs = Manage.objects.filter(
                Q(username__username__icontains=query)|
                Q(username__first_name__icontains=query),
                appear_in_search=True
            )
            context = {'objs': objs}
        return render(request, 'search.html', context)
    return render(request, 'search.html', {})

def www_root_redirect(request, path=None):
    return redirect(host_reverse('home', host='www'))
