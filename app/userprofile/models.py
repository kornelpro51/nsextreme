from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
#from django.contrib.comments.signals import comment_was_posted
from nsextreme.video.models import Video, VideoCategory

"""
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

from app.events.models import Event
from app.timelines.models import Timeline
from app.academy.models import University, UniversityMembership, Course
from allauth.account.signals import email_confirmed, user_signed_up
from allauth.socialaccount.models import SocialToken

from facepy import GraphAPI
"""


class Sports(models.Model):
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

GENDER_CHOICES = (
    (1, 'Male'),
    (2, 'Female'),
)

RELATIONSHEEP_CHOICES = (
    (1, 'Single'),
    (2, 'Married'),
)


class Profile(models.Model):

    user = models.OneToOneField(User)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    picture = models.ImageField(upload_to='images/profiles/', blank=True, null=True)
    title = models.CharField(blank=True, null=True, max_length=200)
    location = models.CharField(blank=True, null=True, max_length=200)

    thumbnail_picture =  models.ImageField(
        upload_to='images/profiles/',
        blank=True, null=True)
    small_picture =  models.ImageField(
        upload_to='images/profiles/',
        blank=True, null=True)

    bio = models.TextField(blank=True, null=True)
    sports = models.ForeignKey('Sports', default=None, blank=True, null=True )
    video_category = models.ForeignKey(VideoCategory, default=None, blank=True, null=True )
    birth_date = models.DateField(blank=True, null=True)
    public_activity = models.BooleanField(default=True)

    favorite_videos = models.ManyToManyField(Video, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    show_welcome = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return self.user.get_absolute_url()

    def get_thumbnail_picture(self):
        res = '%simages/profile-default.jpg' % settings.MEDIA_URL

        try:
            res = self.thumbnail_picture.url
        except:
            pass
        return res

    def get_small_picture(self):
        res = '%simages/profile-default.jpg' % settings.MEDIA_URL

        try:
            res = self.small_picture.url
        except:
            pass
        return res

    def gender_label(self):
        return GENDER_CHOICES[self.gender-1][1]

    @property
    def recentVideos_l(self):
        result = Video.objects.filter(user=self).order_by('-date_created')[:5]
        return result

    @property
    def topVideos_l(self):
        result = Video.objects.filter(user=self).order_by('-recommend')[:5]
        return result

    def recentVideos(self, limit=5, start=0):
        result = Video.objects.filter(user=self).order_by('-date_created')[start:limit]
        return result

    def topVideos(self, limit=5, start=0):
        result = Video.objects.filter(user=self).order_by('-recommend')[start:limit]
        return result


def get_display_name(self):
    if not self.get_full_name():
        return self.username
    return self.get_full_name()
User.add_to_class('display_name', get_display_name)


def is_admin(self):
    return self.is_superuser.filter(role=1).exists()
User.add_to_class('is_admin', is_admin)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)



"""
class Status(models.Model):
    title = models.TextField()
    image = models.ImageField(upload_to='detail/', blank=True, default='')
    thumbnail = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
        ResizeToFill(200, 200)], image_field='image', format='JPEG',
        options={'quality': 90})
    attachment = models.FileField(upload_to='detail/', blank=True, default='')
    url_link = models.URLField(max_length=200)
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class CommentStatus(models.Model):
    status = models.ForeignKey(Status)
    comment = models.TextField()
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.comment


@receiver(email_confirmed)
def setup_universities_upon_registration(email_address, **kwargs):
    user = email_address.user
    email = email_address.email
    username, dom = email.split('@')

    try:
        univ = University.objects.get(domain=dom)
        UniversityMembership.objects.create(university=univ, user=user)
    except:
        univ = University.objects.create(name=dom, description='new university',
                domain=dom)


@receiver(user_signed_up)
def notify_facebook_friends(request, user, **kwargs):
    try:
        user_token = SocialToken.objects.get(app__provider='facebook', account__user=user)
    except:
        return False
    graph = GraphAPI(user_token.token)
    fb_friends = graph.get('me/friends')
    fb_friends_list = []

    for friend in fb_friends['data']:
        fb_friends_list.append(friend['id'])
    users = User.objects.filter(socialaccount__uid__in=fb_friends_list,
            socialaccount__provider='facebook')

    email_content = '<p><a href="%s">%s</a> just joined social network</p>' % (user.get_absolute_url, user.display_name)
    for user in users:
        send_mail('Your friend just joined School network', email_content,
                settings.DEFAULT_FROM_EMAIL, [user.email])
    return True


@receiver(comment_was_posted)
def send_email_comment(sender, comment, request, **kwargs):
    #tmp = kwargs, instance
    #print comment.content_object.created_by.email
    send_mail('New Comment Notification', settings.DEFAULT_CONTENT_EMAIL_COMMENT, settings.DEFAULT_FROM_EMAIL, [comment.content_object.created_by.email])
"""