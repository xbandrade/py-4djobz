from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from jobs.models import Application


class ApplicantDashboardView(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'users/pages/applicant_dashboard.html'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_company:
            return redirect('users:c_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        applications = Application.objects.select_related(
            'applicant_profile'
        ).filter(
            applicant_profile=request.user.applicantprofile
        ).order_by('-id')
        context = {
            'applications': applications,
        }
        return render(request, self.template_name, context=context)
