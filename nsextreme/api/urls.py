import json as simplejson


from django import forms
from django.conf.urls.defaults import patterns, url
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from nsextreme.video import process
from nsextreme.video.models import Video, VideoCategory


# http://superuser.com/questions/233288/curl-upload-file-and-send-post-data
# curl -F 'video=@testvideo.mov' -F 'data=@testvideo.xml' \
#      -F 'title=Test Video' -F 'username=jbb' -F 'password=password' \
#      http://localhost:8000/api/v1/upload_video


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=255, required=False)
    video = forms.FileField()
    data = forms.FileField()
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)


@csrf_exempt
def uploader(request):
    """
    Uploader API

    To be used via HTTPS only

    POST Params:
    - username: string
    - password: string
    - title: string optional
    - video: FILE: video data
    - data: FILE: xml data

    Returns:
    STATUS 200 - success
    403 - authentication failed
    400 - Bad parameters
    """
    if request.method != 'POST':
        return HttpResponse('request must be POST', status=400)

    # Create form instance and validate it
    form = UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return HttpResponse('invalid parameters', status=400)

    # Authenticate the user
    user = authenticate(
        username=request.POST['username'], password=request.POST['password'])
    if not user:
        return HttpResponse("Unauthorized", status=403)
    title = request.POST.get('title') or 'No Title'

    # Read data in from FILES request object
    file_data = request.FILES['data'].read()

    # Convert the file data from JSON string to python object 
    video_data = simplejson.loads(file_data)

    # Extract video data from decoded JSON string
    sports = video_data["video_files"]["sport"]
    shared = not video_data["video_files"]["isPrivate"]

    # Check if category exists
    category = VideoCategory.objects.filter(title=sports)
    if category.exists():
        category = category[0]
    else: 
        # If category doesn't exist, create one
        category = VideoCategory(title=sports)
        category.save()

    # Create and save the video database entry
    video = Video(title=title, 
                  user=user, 
                  video=request.FILES['video'], 
                  data=file_data, 
                  shared=shared, 
                  category=category)
    video.save()

    # Process the uploaded file (generate thumbnail, etc)
    process.process_upload(video)

    user.video_category = category 
    user.save()

    return HttpResponse('ok')


urlpatterns = patterns(
    '',
    url(r'^v1/upload_video', uploader),
    # url(r'^posts/$', blogposts),
    # url(r'^posts/(?P<emitter_format>.+)/$', blogposts),
    # url(r'^posts\.(?P<emitter_format>.+)', blogposts, name='blogposts'),

    # # automated documentation
    # url(r'^$', documentation_view),
)
    