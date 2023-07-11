from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from jobs.forms import PublishForm
from jobs.models import Job


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class JobUpdateView(View):
    template_name = 'jobs/pages/update.html'

    def get(self, request, pk):
        try:
            job = Job.objects.get(
                id=pk, company_profile__user=request.user)
        except Job.DoesNotExist:
            raise Http404()
        form = PublishForm(instance=job)
        context = {
            'form': form,
            'job': job,
        }
        return render(self.request, self.template_name, context)

    def post(self, request, pk):
        try:
            job = Job.objects.get(
                id=pk, company_profile__user=request.user)
        except Job.DoesNotExist:
            raise Http404()
        form = PublishForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, _('Job updated successfully'))
            return redirect(reverse('users:c_dashboard'))
        messages.error(request, _('Failed to update job'))
        context = {
            'form': form,
            'job': job,
        }
        return render(self.request, self.template_name, context)
