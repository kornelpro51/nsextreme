import os


from django.contrib.auth.models import User


#from bookmarks.handlers import library


#library.register(Video)


"""
class UserProfile(models.Model):
    GENDER = (
        ('f', 'Female'),
        ('m', 'Male'),
    )
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.ImageField(
        upload_to='image/profiles/%Y/%m/',
        blank=True, null=True)
    home_location = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    default_sport = models.CharField(max_length = 50)
    gender = models.CharField(max_length=1, choices=GENDER)
    date_created = models.DateField(auto_now_add=True)

    def _get_full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    full_name = property(_get_full_name)

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })

    get_absolute_url = models.permalink(get_absolute_url)
"""

#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

