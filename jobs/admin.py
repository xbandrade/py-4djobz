from django.contrib import admin

from .models import Application, Job


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company_name',
                    'salary', 'minimum_education', 'created_date')


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'applicant_email', 'applicant_name',
                    'applicant_education', 'salary_expectations',
                    'applicant_experiences', 'applied_date')


admin.site.register(Job, JobAdmin)
admin.site.register(Application)
