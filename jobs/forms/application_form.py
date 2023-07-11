from django import forms
from django.utils.translation import gettext_lazy as _

from jobs.models import Application
from utils import MIN_EDUCATION_CHOICES, SALARY_CHOICES


class ApplicationForm(forms.ModelForm):
    salary_expectations = forms.ChoiceField(
        choices=SALARY_CHOICES,
        required=True,
        label=_('Salary Expectations *'),
    )
    applicant_education = forms.ChoiceField(
        choices=MIN_EDUCATION_CHOICES,
        required=True,
        label=_('Minimum Education *'),
    )
    applicant_experiences = forms.CharField(
        error_messages={
            'required': _('Experiences is required'),
        },
        required=True,
        widget=forms.Textarea,
        label=_('Your Experiences *'),
    )

    class Meta:
        model = Application
        fields = ['applicant_education', 'salary_expectations',
                  'applicant_experiences']

    def clean(self):
        cleaned_data = super().clean()
        job = cleaned_data.get('job')
        applicant_profile = cleaned_data.get('applicant_profile')
        if job and applicant_profile:
            existing_applications = Application.objects.filter(
                job=job, applicant_profile=applicant_profile)
            if existing_applications.exists():
                raise forms.ValidationError(
                    _('You have already applied to this job.'))
        return cleaned_data
