"""Custom urls.py for django-registration."""

from django.conf import settings
from django.conf.urls import include, url, patterns
from django.views.generic import TemplateView

from registration.backends.default.views import (
    ActivationView,
    RegistrationView,
)

from nsextreme.reg.forms import EmailRegistrationForm
from nsextreme.reg.views import ReactivationView

urlpatterns = patterns(
    '',
    url(r'^activate/',
        ReactivationView.as_view(),
        name='nsextreme_reg_reactivate'
        ),
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(
            template_name='registration/activate.html',
        ),
        name='registration_activate'),
    url(r'^register/$',
        RegistrationView.as_view(
            form_class=EmailRegistrationForm,
        ),
        name='registration_register'),
)
