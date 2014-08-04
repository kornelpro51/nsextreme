from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
"""
from friendship.models import Friend
from postman.models import Message

from .forms import EditProfileForm, UserListForm, PersonalEventForm, InterestForm, HobbyForm
from .models import Profile, Interest, Hobby

from app.academy.models import Course
from app.timelines.forms import *
from app.events.models import Event

from datetime import datetime
"""
from .forms import EditProfileForm
from .models import Profile


def main(request, template='userprofile/index.html'):

    if request.user.is_authenticated():
        return HttpResponseRedirect(''+request.user.get_absolute_url())

    variables = RequestContext(request, {})
    return render(request, template, variables)


@login_required
def profile_detail(request, username, template='userprofile/shared.html'):
    user = get_object_or_404(User, username=username, is_active=True)

    variables = RequestContext(request, {
        'person': user,
    })
    return render(request, template, variables)


@login_required
def edit(request, username, template='userprofile/edit.html'):
    if username != request.user.username:
        return HttpResponseRedirect(''+request.user.get_absolute_url())

    user = get_object_or_404(User, is_active=True, username=username)

    user_profile, created = Profile.objects.get_or_create(user=user)
    show_welcome = False

    if request.user != user:
        raise Http404('You are not allowed to edit this page')

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            # use existing profile instead of creating one
            profile = form.save()

            profile.user.username = cleaned_data.get('username')
            profile.user.first_name = cleaned_data.get('first_name')
            profile.user.last_name = cleaned_data.get('last_name')
            profile.user.location = cleaned_data.get('location')
            profile.user.save()
            return HttpResponseRedirect(reverse('userprofile_edit', args=[profile.user.username]))

    else:
        show_welcome = user_profile.show_welcome
        if user_profile.show_welcome:
            user_profile.show_welcome = False
            user_profile.save()
        initial_data = {
            'user': user,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
        }
        form = EditProfileForm(initial=initial_data, instance=user_profile)

    print(show_welcome)

    variables = RequestContext(request, {
        'form': form,
        'show_welcome': show_welcome
    })
    return render(request, template, variables)



