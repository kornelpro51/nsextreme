from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Profile
from .widgets import AdminImageWidget


class UserListForm(forms.Form):
    username = forms.ModelChoiceField(queryset=User.objects.all())


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile

    username = forms.CharField(label=_('Username'), widget=forms.HiddenInput())
    first_name = forms.CharField(label=_('First name'))
    last_name = forms.CharField(label=_('Last name'))
    location = forms.CharField(label=_('Location'), required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    picture = forms.ImageField(
        label="",
        widget = AdminImageWidget(default_image='/media/images/profile-default.jpg'),
        required=False
    )
    #def clean_username(self):
    #    if self.instance.pk:
    #        q = User.objects.filter(
    #            username=self.cleaned_data['username']
    #        ).exclude(id=self.instance.pk)
    #        if q:
    #            raise forms.ValidationError(_('User with the same username already exists'))
    #    return self.cleaned_data['username']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'username',
            'picture',
            'first_name',
            'last_name',
            'title',
            'location',
            'bio',
            'gender',
            #'sports',
            'birth_date',
            'user']


