from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View

from jobs.models import Job


class CompanyDashboardView(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'users/pages/company_dashboard.html'
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_company:
            return redirect('users:u_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Job.objects.filter(
            company_profile=self.request.user.companyprofile)
        queryset = queryset.select_related('company_profile')
        queryset = queryset.annotate(application_count=Count('applications'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_job(self, id=None):
        job = None
        if not self.request.user.is_company:
            raise Http404()
        if id:
            job = Job.objects.filter(
                company_profile=self.request.user.companyprofile,
                id=id,
            ).first()
            if not job:
                raise Http404()
        return job

    def get(self, request):
        jobs = self.get_queryset().order_by('-id')
        context = {
            'jobs': jobs,
        }
        return render(request, self.template_name, context=context)


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardJobDelete(CompanyDashboardView):
    def post(self, *args, **kwargs):
        job = self.get_job(self.request.POST.get('id'))
        if not job:
            messages.warning(self.request, _('Job post not found'))
        else:
            job.delete()
            messages.success(self.request, _('Job post successfully deleted'))
        return redirect(reverse('users:c_dashboard'))
