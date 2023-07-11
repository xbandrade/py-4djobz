from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from jobs.models import Application, Job


class JobApplicantsView(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'jobs/pages/applicants.html'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_company:
            return redirect('users:u_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        job = get_object_or_404(
            Job, id=pk, company_profile=request.user.companyprofile)
        applications = Application.objects.filter(job=job).order_by('id')

        sort_by_compatibility = request.GET.get('sort_by_compatibility')
        if sort_by_compatibility:
            applications = applications.order_by('-compatibility')

        context = {
            'job': job,
            'applications': applications,
            'sort_by_compatibility': sort_by_compatibility,
        }
        return render(request, self.template_name, context=context)
