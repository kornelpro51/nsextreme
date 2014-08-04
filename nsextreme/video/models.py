from django.contrib.auth.models import User
from django.db import models


from nsextreme.video import process


class VideoCategory(models.Model):
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class VideoComment(models.Model):
    content = models.CharField(max_length=3000)
    recommend = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey('Video', default=None, blank=True, null=True)
    created_by = models.ForeignKey(User, default=None, blank=True, null=True)

    def __unicode__(self):
        return self.content[0:5]


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500,default=None, blank=True, 
        null=True)
    user = models.ForeignKey(User)
    video = models.FileField(upload_to='video/original/%Y/%m/')
    thumbnail = models.ImageField(upload_to='video/thumbs/%Y/%m/',blank=True, 
        null=True)
    data = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    #comment = models.ManyToManyField(VideoComment, default=None, blank=True, null=True)
    category = models.ForeignKey(VideoCategory, default=None, blank=True, 
        null=True)
    shared = models.BooleanField(default=0)
    visits = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    unlikes = models.IntegerField(default=0)
    recommend = models.IntegerField(default=0)

    is_removed = models.BooleanField(default=0)

    @models.permalink
    def get_absolute_url(self):
        return ('nsextreme.views.details', [str(self.id)])

    @models.permalink
    def get_private_url(self):
        return ('nsextreme.views.private_video', [str(self.id)])

    def delete(self, *args, **kwargs):
        # delete associated file when model is deleted
        self.video.delete()
        self.thumbnail.delete()
        super(Video, self).delete(*args, **kwargs)

    def recentComments(self):
        return VideoComment.objects.filter(video=self) \
            .order_by('-created_at')

    def topComments(self):
        return VideoComment.objects.filter(video=self) \
            .order_by('-recommend', 'created_at')

    @classmethod
    def latest(cls, amount):
        return cls.objects.filter(shared=True).exclude(is_removed=True) \
            .order_by('-date_created')[:amount]
