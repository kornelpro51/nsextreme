import os
import hashlib

from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.conf import settings


class Email(forms.EmailField):
    def clean(self, value):
        super(Email, self).clean(value)
        try:
            User.objects.get(email=value)
            raise forms.ValidationError("This email is already registered. Use the 'forgot password' link on the login page")
        except User.DoesNotExist:
            return value


def get_md5_hexdigest(email):
    """
    Returns an md5 hash for a given email.

    The length is 30 so that it fits into Django's ``User.username`` field.

    """
    if isinstance(email, str):  # for py3
        email = email.encode('utf-8')
    return hashlib.md5(email).hexdigest()[0:30]


def generate_username(email):
    """
    Generates a unique username for the given email.

    The username will be an md5 hash of the given email. If the username exists
    we just append `a` to the email until we get a unique md5 hash.

    """
    try:
        User.objects.get(email=email)
        raise Exception('Cannot generate new username. A user with this email'
                        'already exists.')
    except User.DoesNotExist:
        pass

    emailPartials = email.split("@")
    emailName = emailPartials[0]
    username = emailName

    idx = 1

    found_unique_username = False

    while not found_unique_username:
        try:
            User.objects.get(username=username)
            username = emailName + "_" +str(idx)
        except User.DoesNotExist:
            found_unique_username = True
            return username


attrs_dict = {'class': 'required'}


class EmailRegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """

    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=256)),
        label=_("Email")
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label=_("Password")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label=_("Password (repeat)"))
    your_name = forms.CharField(required=False)

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        email = self.cleaned_data['email'].strip()
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email.lower()
        raise forms.ValidationError(
            _('A user with that email already exists.'))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields match.

        Note that an error here will end up in ``non_field_errors()`` because
        it doesn't apply to a single field.

        """
        data = self.cleaned_data
        if data.get('your_name'):
            # Bot protection. The name field is not visible for human users.
            raise forms.ValidationError(_('Please enter a valid name.'))
        if not 'email' in data:
            return data
        if ('password1' in data and 'password2' in data):

            if data['password1'] != data['password2']:
                raise forms.ValidationError(
                    _("The two password fields didn't match."))

        self.cleaned_data['username'] = generate_username(data['email'])
        return self.cleaned_data

    class Media:
        css = {
            'all': (os.path.join(
                settings.STATIC_URL, 'registration_email/css/auth.css'), )
        }

class EmailReactivationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=256)),
        label=_("Please input your Email address")
    )
    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        email = self.cleaned_data['email'].strip()
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise forms.ValidationError(
                _('Any registered user does not use this email address.'))
        return email.lower()
