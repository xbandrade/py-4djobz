from django import forms
from django.utils.translation import gettext_lazy as _

from jobs.models import Job
from utils import MIN_EDUCATION_CHOICES, SALARY_CHOICES


class PublishForm(forms.ModelForm):
    title = forms.CharField(
        error_messages={
            'required': _('Job title cannot be empty'),
        },
        required=True,
        label=_('Job Title *'),
    )
    salary = forms.ChoiceField(
        choices=SALARY_CHOICES,
        required=True,
        label=_('Salary *'),
    )
    minimum_education = forms.ChoiceField(
        choices=MIN_EDUCATION_CHOICES,
        required=True,
        label=_('Minimum Education *'),
    )
    skill_requirements = forms.CharField(
        error_messages={
            'required': _('Skill requirements is required'),
        },
        required=True,
        label=_('Skill Requirements *'),
        widget=forms.Textarea,
    )
    is_finished = forms.BooleanField(
        required=False,
        label=_('Mark job post as finished'),
    )

    class Meta:
        model = Job
        fields = ['title', 'salary', 'skill_requirements',
                  'minimum_education', 'hide_salary', 'is_finished']
