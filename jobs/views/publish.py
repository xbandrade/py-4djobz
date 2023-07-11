from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from jobs.forms import PublishForm


class JobPublishView(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'jobs/pages/publish.html'
    redirect_field_name = 'next'

    def get(self, request):
        if not request.user.is_company:
            raise Http404()
        form = PublishForm()
        context = {
            'form': form,
        }
        return render(
            self.request,
            self.template_name,
            context
        )

    def post(self, request):
        if not request.user.is_company:
            raise Http404()
        form = PublishForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company_profile = request.user.companyprofile
            job.save()
            messages.success(request, _('Job published successfully'))
            return redirect(reverse('users:c_dashboard'))
        messages.error(request, _('Failed to publish job'))
        return render(self.request, self.template_name)
