import json
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View

from jobs.models import Application, Job


class CompanyChartsView(LoginRequiredMixin, View):
    template_name = 'users/pages/company_charts.html'
    context_object_name = 'company'

    def get_queryset(self):
        company_profile = self.request.user.companyprofile

        today = datetime.now().date()
        start_date = today - timedelta(days=29)

        job_queryset = Job.objects.filter(
            company_profile=company_profile,
            created_date__date__range=(start_date, today)
        ).values('created_date__date').annotate(
            count=Count('id')
        ).order_by('created_date__date')

        application_queryset = Application.objects.filter(
            job__company_profile=company_profile,
            applied_date__date__range=(start_date, today)
        ).values('applied_date__date').annotate(
            count=Count('id')
        ).order_by('applied_date__date')

        queryset1 = [
            {'created_date__date': item['created_date__date'],
             'count': item['count']}
            for item in job_queryset
        ]

        queryset2 = [
            {'applied_date__date': item['applied_date__date'],
             'count': item['count']}
            for item in application_queryset
        ]

        return queryset1, queryset2

    def get(self, request):
        if not request.user.is_company:
            raise Http404()

        queryset1, queryset2 = self.get_queryset()
        chart_data1 = json.dumps(queryset1, cls=DjangoJSONEncoder)
        chart_data2 = json.dumps(queryset2, cls=DjangoJSONEncoder)
        context = {
            'chart_data1': chart_data1,
            'chart_data2': chart_data2,
        }
        return render(request, self.template_name, context=context)
