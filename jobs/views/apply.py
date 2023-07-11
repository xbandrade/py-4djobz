from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View

from jobs.forms import ApplicationForm
from jobs.models import Application, Job


class JobApplyView(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'jobs/pages/apply.html'
    redirect_field_name = 'next'

    def get(self, request, pk):
        if request.user.is_company:
            raise Http404()
        job = get_object_or_404(Job, pk=pk)
        if job.is_finished:
            raise Http404()
        applicant_profile = request.user.applicantprofile
        context = {
            'job': job,
        }
        if Application.objects.filter(
                job=job, applicant_profile=applicant_profile).exists():
            context['already_applied'] = True
        else:
            context['form'] = ApplicationForm()
        return render(
            self.request,
            self.template_name,
            context
        )

    def post(self, request, pk):
        if request.user.is_company:
            raise Http404()
        job = get_object_or_404(Job, pk=pk)
        if job.is_finished:
            raise Http404()
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant_profile = request.user.applicantprofile
            application.save()
            messages.success(
                request,
                _('Application submitted successfully, '
                  'you will be contacted via email or phone call shortly '
                  'with the feedback'))
            return redirect(reverse('users:u_dashboard'))
        messages.error(request, _('Failed to submit application'))
        context = {
            'form': form,
            'job': job,
        }
        return render(self.request, self.template_name, context)
