import json
import time
from datetime import datetime, date, timedelta, time

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django import forms
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

from nsextreme.video.models import Video, VideoCategory, VideoComment
from nsextreme.forms import CommentForm, ShareEmailForm, VideoEditForm

######################################################################
COUNT_PER_PAGE = 8
# Create your views here.


def details(request, pk):
    video = get_object_or_404(Video, pk=pk)
    latest_videos = Video.latest(5)
    # latest_videos = Video.objects.filter(user=video.user)
    video.visits = video.visits + 1
    video.save()
    return render(request, 'video_detail.html',
        {'video': video, 'latest_videos': latest_videos, 'page_name': 'explore'})


@login_required
def video_edit(request, videoid, template='video_detail_edit.html'):
    video = get_object_or_404(Video, pk=videoid, user_id=request.user.id)

    if request.method == 'POST':
        form = VideoEditForm(request.POST, request.FILES, instance=video)

        if form.is_valid():
            # use existing profile instead of creating one
            form.save()

            return HttpResponseRedirect(reverse('private_video', args=[videoid]))

    else:
        video = get_object_or_404(Video, pk=videoid, user_id=request.user.id)
        frm = VideoEditForm(instance=video)

    return render(request, template, {'video': video, 'form': frm})


@login_required
def video_delete(request, videoid, template='video_detail_edit.html'):
    video = get_object_or_404(Video, pk=videoid, user_id=request.user.id)
    video.is_removed = True
    video.save()
    return HttpResponseRedirect(reverse('activity'))


@login_required
def video_share(request, videoid):
    video = get_object_or_404(Video, pk=videoid, user_id=request.user.id)

    if video.shared == True:
        video.shared = False
    else:
        video.shared = True
    video.save()
    return HttpResponse(json.dumps({'success': True, 'shared': video.shared}), content_type="application/json")


@login_required
def private_video(request, videoid, template='video_detail_private.html'):

    video = get_object_or_404(Video, pk=videoid, user_id=request.user.id)
    latest_videos = Video.latest(5)
    # latest_videos = Video.objects.filter(user=video.user)
    return render(request, template,
        {'video': video, 'latest_videos': latest_videos, 'page_name': 'activity'})


def video_data(request, pk):
    video = get_object_or_404(Video, pk=pk)
    filename = video.video.name.split('/')[-1]
    response = HttpResponse(video.video, content_type='video/mp4')

    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


def sensor_data(request, pk):
    pass


def scanner(request):
    from nsextreme import thumbnail_scanner
    thumbnail_scanner()
    return HttpResponse('ok')

######################################################################


def share_via_email(request, pk):
    if request.method != 'POST':
        return HttpResponse('request must be POST', status=400)
    video = get_object_or_404(Video, pk=pk)
    form = ShareEmailForm(request.POST)
    if not form.is_valid():
        return HttpResponse(json.dumps({'errors': form.errors['email'][0]}),
                            content_type="application/json")
    email = request.POST['email']
    video_url = request.build_absolute_uri(video.get_absolute_url())
    send_mail(
        'NSExtreme: Video shared with you!', 'A video was shared with you: %s' % (
            video_url), request.user.email, (email,))
    return HttpResponse(json.dumps({}), content_type="application/json")

#########################################################################


def home(request):
    return render(request, 'homepage.html', {'page_name': 'home'})


def features(request):
    return render(request, 'static/features.html', {'page_name': 'features'})


def testimonials(request):
    return render(request, 'static/testimonials.html', {'page_name': 'testimonials'})


def terms_conditions(request):
    return render(request, 'static/terms_conditions.html', {'page_name': 'terms_conditions'})


def contact(request):
    return render(request, 'static/contact.html', {'page_name': 'contact'})


def support(request):
    return render(request, 'static/support.html', {'page_name': 'support'})

############################################################################

@login_required
def profile(request):
    message = ""
    if request.user.profile:
        message = "welcome"
    else:
        message = "You are first login"
        request.user.profile

    return render(request, 'profile.html', {'page_name': 'profile', 'msg': message , 'profile': request.user.profile})

#####################################################################


def explore(request, template='explore.html'):
    category_list = VideoCategory.objects.all()

    videos = Video.objects.filter(shared=True).exclude(is_removed=True).order_by('-date_created')
    if videos.count() <= COUNT_PER_PAGE:
        next_page_url = None
        video_list = videos
    else:
        next_page_url = reverse('explore_p', args=[2])
        video_list = videos[:COUNT_PER_PAGE]

    return render(request, template, {'category_list' : category_list, 'current_category': None, 'video_list' : video_list, 'page_name': 'explore', 'next_page' : next_page_url})


def explore_p(request, pagenum, template='explore_page.html'):
    videos = Video.objects.filter(shared=True).exclude(is_removed=True).order_by('-date_created')
    paginator = Paginator(videos, COUNT_PER_PAGE)
    cur_page = int(pagenum)
    try:
        video_list = paginator.page(pagenum)
    except PageNotAnInteger:
        video_list = paginator.page(1)
    except EmptyPage:
        video_list = paginator.page(paginator.num_pages)

    try:
        next_page = video_list.next_page_number()
        next_page_url = reverse('explore_p', args=[next_page])
    except InvalidPage:
        next_page_url = None

    return render(request, template, {'next_page' : next_page_url, 'video_list' : video_list})


def explore_c(request, categoryid, template='explore.html'):
    #category_list = VideoCategory.objects.all()
    #video_list = Video.objects.filter(shared=True,category_id=categoryid).order_by('-date_created')
    #return render(request, template, {'category_list' : category_list, 'current_category': int(categoryid), 'video_list' : video_list, 'page_name': 'explore'})

    category_list = VideoCategory.objects.all()
    videos = Video.objects.filter(shared=True, category_id=categoryid).exclude(is_removed=True).order_by('-date_created')

    if videos.count() <= COUNT_PER_PAGE:
        next_page_url = None
        video_list = videos
    else:
        next_page_url = reverse('explore_c_p', args=[categoryid, 2])
        video_list = videos[:COUNT_PER_PAGE]

    return render(request, template, {'category_list' : category_list, 'current_category': int(categoryid), 'video_list': video_list, 'page_name': 'explore', 'next_page': next_page_url})


def explore_c_p(request, categoryid, pagenum, template='explore_page.html'):
    videos = Video.objects.filter(shared=True, category_id=categoryid).exclude(is_removed=True).order_by('-date_created')
    paginator = Paginator(videos, COUNT_PER_PAGE)
    cur_page = int(pagenum)
    try:
        video_list = paginator.page(pagenum)
    except PageNotAnInteger:
        video_list = paginator.page(1)
    except EmptyPage:
        video_list = paginator.page(paginator.num_pages)

    try:
        next_page = video_list.next_page_number()
        next_page_url = reverse('explore_c_p', args=[categoryid, next_page])
    except InvalidPage:
        next_page_url = None

    return render(request, template, { 'next_page' : next_page_url, 'video_list' : video_list})


@login_required
def activity(request, template='activity.html'):
    category_list = VideoCategory.objects.all()

    videos = Video.objects.filter(user_id=request.user.id).exclude(is_removed=True).order_by('-date_created')
    if videos.count() <= COUNT_PER_PAGE:
        next_page_url = None
        video_list = videos
    else:
        next_page_url = reverse('activity_p', args=[2])
        video_list = videos[:COUNT_PER_PAGE]

    return render(request, template, {'category_list' : category_list, 'current_category': None, 'video_list' : video_list, 'page_name': 'activity', 'next_page' : next_page_url})


@login_required
def activity_p(request, pagenum, template='activity_page.html'):

    videos = Video.objects.filter(user_id=request.user.id).exclude(is_removed=True).order_by('-date_created')

    paginator = Paginator(videos, COUNT_PER_PAGE)
    cur_page = int(pagenum)
    try:
        video_list = paginator.page(pagenum)
    except PageNotAnInteger:
        video_list = paginator.page(1)
    except EmptyPage:
        video_list = paginator.page(paginator.num_pages)

    try:
        next_page = video_list.next_page_number()
        next_page_url = reverse('activity_p', args=[next_page])
    except InvalidPage:
        next_page_url = None

    return render(request, template, {'next_page' : next_page_url, 'video_list' : video_list})

@login_required
def activity_c(request, categoryid, template='activity.html'):
    category_list = VideoCategory.objects.all()
    video_list = Video.objects.filter(category_id=categoryid)
    return render(request, template, {'category_list' : category_list, 'current_category': int(categoryid), 'video_list' : video_list, 'page_name': 'activity'})

@login_required
def activity_c_p(request, categoryid, pagenum, template='activity.html'):
    category_list = VideoCategory.objects.all()
    video_list = Video.objects.filter(category_id=categoryid)
    return render(request, template, {'category_list' : category_list, 'current_category': int(categoryid), 'video_list' : video_list, 'page_name': 'activity'})

@login_required
def favorites(request, template='explore.html'):
    #category_list = VideoCategory.objects.all()
    #video_list = request.user.profile.favorite_videos.all()
    #return render(request, template, {'category_list' : category_list, 'current_category': 'favorites', 'video_list' : video_list, 'page_name': 'activity'})

    category_list = VideoCategory.objects.all()

    videos = request.user.profile.favorite_videos.all().order_by('-date_created')
    if videos.count() <= COUNT_PER_PAGE:
        next_page_url = None
        video_list = videos
    else:
        next_page_url = reverse('favorites_p', args=[2])
        video_list = videos[:COUNT_PER_PAGE]

    return render(request, template, {'category_list' : category_list, 'current_category': 'favorites', 'video_list' : video_list, 'page_name': 'favorites', 'next_page' : next_page_url})

@login_required
def favorites_p(request, pagenum, template='explore_page.html'):
    #category_list = VideoCategory.objects.all()
    #video_list = request.user.profile.favorite_videos.all()
    #return render(request, template, {'category_list' : category_list, 'current_category': 'favorites', 'video_list' : video_list, 'page_name': 'activity'})

    videos = request.user.profile.favorite_videos.all().order_by('-date_created')
    paginator = Paginator(videos, COUNT_PER_PAGE)
    cur_page = int(pagenum)
    try:
        video_list = paginator.page(pagenum)
    except PageNotAnInteger:
        video_list = paginator.page(1)
    except EmptyPage:
        video_list = paginator.page(paginator.num_pages)

    try:
        next_page = video_list.next_page_number()
        next_page_url = reverse('favorites_p', args=[next_page])
    except InvalidPage:
        next_page_url = None

    return render(request, template, {'next_page' : next_page_url, 'video_list' : video_list})

@login_required
def favorites_add(request):
    if request.method != 'POST':
        return HttpResponse('request must be POST', status=400)

    videoid = request.POST.get('videoid')
    video = get_object_or_404(Video, pk=videoid)

    request.user.profile.favorite_videos.add(video)
    request.user.profile.save()

    result = {}
    result['success'] = True

    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
def favorites_remove(request):
    if request.method != 'POST':
        return HttpResponse('request must be POST', status=400)

    videoid = request.POST.get('videoid')
    video = get_object_or_404(Video, pk=videoid)

    request.user.profile.favorite_videos.remove(video)
    request.user.profile.save()

    result = {}
    result['success'] = True
    return HttpResponse(json.dumps(result), content_type="application/json")


@login_required
def popular(request, template='explore.html'):
    category_list = VideoCategory.objects.all()
    video_list = Video.objects.all().order_by('-visits')
    return render(request, template, {'category_list' : category_list, 'current_category': 'popular', 'video_list' : video_list, 'page_name': 'activity'})

@login_required
def popular_p(request, pagenum, template='explore.html'):
    category_list = VideoCategory.objects.all()
    video_list = Video.objects.all().order_by('-visits')
    return render(request, template, {'category_list' : category_list, 'current_category': 'popular', 'video_list' : video_list, 'page_name': 'activity'})


@login_required
def toppicks(request, template='explore.html'):
    #category_list = VideoCategory.objects.all()
    #today = date.today()
    #a_week_ago = today.min() + timedelta(days=7);
    #video_list = Video.objects.filter(meeting_datetime__gt=a_week_ago).order_by('-recommend')
    #return render(request, template, {'category_list' : category_list, 'current_category': 'toppicks', 'video_list' : video_list, 'page_name': 'activity'})
    category_list = VideoCategory.objects.all()

    today_min = datetime.combine(date.today(), time.min)
    a_week_ago = today_min - timedelta(days=7)
    videos = Video.objects.filter(date_created__gt=a_week_ago).order_by('-visits')

    if videos.count() <= COUNT_PER_PAGE:
        next_page_url = None
        video_list = videos
    else:
        next_page_url = reverse('toppicks_p', args=[2])
        video_list = videos[:COUNT_PER_PAGE]

    return render(request, template, {'category_list' : category_list, 'current_category': 'toppicks', 'video_list' : video_list, 'page_name': 'explore', 'next_page' : next_page_url})


@login_required
def toppicks_p(request, pagenum, template='explore_page.html'):
    #category_list = VideoCategory.objects.all()
    #video_list = Video.objects.all().order_by('-recommend')
    #return render(request, template, {'category_list' : category_list, 'current_category': 'toppicks', 'video_list' : video_list, 'page_name': 'activity'})
    today_min = datetime.combine(date.today(), time.min)
    a_week_ago = today_min - timedelta(days=7)
    videos = Video.objects.filter(date_created__gt=a_week_ago).order_by('-visits')

    paginator = Paginator(videos, COUNT_PER_PAGE)
    cur_page = int(pagenum)
    try:
        video_list = paginator.page(pagenum)
    except PageNotAnInteger:
        video_list = paginator.page(1)
    except EmptyPage:
        video_list = paginator.page(paginator.num_pages)

    try:
        next_page = video_list.next_page_number()
        next_page_url = reverse('toppicks_p', args=[next_page])
    except InvalidPage:
        next_page_url = None

    return render(request, template, {'next_page' : next_page_url, 'video_list' : video_list})


@login_required
def recommended(request, template='explore.html'):
    #category_list = VideoCategory.objects.all()
    #video_list = Video.objects.all().order_by('-recommend')
    #return render(request, template, {'category_list' : category_list, 'current_category': 'recommended', 'video_list' : video_list, 'page_name': 'activity'})
    category_list = VideoCategory.objects.all()

    today_min = datetime.combine(date.today(), time.min)
    a_week_ago = today_min - timedelta(days=7)
    videos = Video.objects.filter(date_created__gt=a_week_ago).order_by('-recommend')

    if videos.count() <= COUNT_PER_PAGE:
        next_page_url = None
        video_list = videos
    else:
        next_page_url = reverse('recommended_p', args=[2])
        video_list = videos[:COUNT_PER_PAGE]

    return render(request, template, {'category_list' : category_list, 'current_category': 'recommended', 'video_list' : video_list, 'page_name': 'explore', 'next_page' : next_page_url})


@login_required
def recommended_p(request, pagenum, template='explore.html'):
    #category_list = VideoCategory.objects.all()
    #video_list = Video.objects.all().order_by('-recommend')
    #return render(request, template, {'category_list' : category_list, 'current_category': 'recommended', 'video_list' : video_list, 'page_name': 'activity'})
    today_min = datetime.combine(date.today(), time.min)
    a_week_ago = today_min - timedelta(days=7)
    videos = Video.objects.filter(date_created__gt=a_week_ago).order_by('-recommend')

    paginator = Paginator(videos, COUNT_PER_PAGE)
    cur_page = int(pagenum)
    try:
        video_list = paginator.page(pagenum)
    except PageNotAnInteger:
        video_list = paginator.page(1)
    except EmptyPage:
        video_list = paginator.page(paginator.num_pages)

    try:
        next_page = video_list.next_page_number()
        next_page_url = reverse('recommended_p', args=[next_page])
    except InvalidPage:
        next_page_url = None

    return render(request, template, {'next_page' : next_page_url, 'video_list' : video_list})

####################################################################

@login_required
def comment_list(request, categoryid, template='activity.html'):
    category_list = VideoCategory.objects.all()
    video_list = Video.objects.filter(category_id=categoryid)
    return render(request, template, {'category_list' : category_list, 'video_list' : video_list, 'page_name': 'activity'})

@login_required
def comment_create(request, videoid):
    if request.method != 'POST':
        return HttpResponse('request must be POST', status=400)

    form = CommentForm(request.POST)
    if not form.is_valid():
        return HttpResponse('invalid parameters', status=400)
    comment = VideoComment(content=request.POST.get('content'), created_by=request.user, video_id=videoid)
    comment.save()
    video = Video.objects.get(id=videoid)
    result = {}
    result['success'] = True
    result['recent'] = render_to_string('comment_list.html', {'comments' : video.recentComments()})
    result['top'] = render_to_string('comment_list.html', {'comments' : video.topComments()})

    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required
def comment_vote(request, commentid):
    if request.method != 'POST':
        return HttpResponse('request must be POST', status=400)
    if not request.POST.get('mode'):
        return HttpResponse('invalid parameters', status=400)

    if not request.POST.get('mode') == 'like' and not request.POST.get('mode') == 'unlike':
        return HttpResponse('invalid parameters', status=400)

    comment = VideoComment.objects.get(id=commentid)
    if request.POST.get('mode') == 'like':
        comment.recommend = comment.recommend + 1
    else:
        comment.recommend = comment.recommend - 1
    comment.save()

    return HttpResponse(json.dumps({'success': True, 'recommend': comment.recommend}), content_type="application/json")

###############################################################################

@login_required
def comment_update(request, commentid, template='activity.html'):
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")

@login_required
def video_like(request, videoid, template='activity.html'):
    video = get_object_or_404(Video, pk=videoid)
    video.likes += 1
    video.recommend += 1
    video.save()
    return HttpResponse(json.dumps({'success': True, 'likes': video.likes, 'recommend': video.recommend}), content_type="application/json")

@login_required
def video_unlike(request, videoid, template='activity.html'):
    video = get_object_or_404(Video, pk=videoid)
    video.unlikes += 1
    video.recommend -= 1
    video.save()
    return HttpResponse(json.dumps({'success': True, 'unlikes': video.unlikes, 'recommend': video.recommend}), content_type="application/json")

@login_required
def video_fav(request, videoid, template='activity.html'):
    if request.method != 'POST':
        return HttpResponse('request must be POST', status=400)

    video = get_object_or_404(Video, pk=videoid)
    if request.POST.get('mode') == 'fav':
        request.user.profile.favorite_videos.remove(video)
        resultStatus = 'none'
    else:
        request.user.profile.favorite_videos.add(video)
        resultStatus = 'fav'

    request.user.profile.save()
    return HttpResponse(json.dumps({'success': True, 'status': resultStatus}), content_type="application/json")

@login_required
def video_list_favorite(request, videoid, template='activity.html'):
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")

@login_required
def video_list_popular(request, videoid, template='activity.html'):

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")

@login_required
def video_list_top_picks(request, videoid, template='activity.html'):
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")

@login_required
def video_list_recommended(request, videoid, template='activity.html'):
    return HttpResponse(json.dumps({'success': True}), content_type="application/json")

