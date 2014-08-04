# Create your views here.
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.shortcuts import render

from registration.models import RegistrationProfile

from forms import EmailReactivationForm


class ReactivationView(TemplateView):

    form_class = EmailReactivationForm
    initial = {'key': 'value'}
    template_name = 'registration/activation_resend.html'


    def post(self, request, *args, **kwargs):
        form = EmailReactivationForm(request.POST)
        msg = ""
        if form.is_valid():
            if Site._meta.installed:
                site = Site.objects.get_current()
            else:
                site = RequestSite(request)
            user = User.objects.get(email=form.clean_email())
            profile = RegistrationProfile.objects.get(user=user)
            profile.send_activation_email(site)
            msg = "* You will receive a confirmation email shortly."

        return self.render_to_response(self.get_context_data(form=form, msg=msg))

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self.render_to_response(self.get_context_data(form=form))
