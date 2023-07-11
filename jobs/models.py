from django.db import models

from users.models import ApplicantProfile, CompanyProfile
from utils import is_education_compatible, is_salary_compatible


class Job(models.Model):
    company_profile = models.ForeignKey(
        CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=100)
    salary = models.CharField(max_length=30)
    skill_requirements = models.TextField()
    minimum_education = models.CharField(max_length=40)
    hide_salary = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def company_name(self):
        return self.company_profile.name

    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='applications')
    applicant_profile = models.ForeignKey(
        ApplicantProfile,
        on_delete=models.CASCADE,
        related_name='applications')
    applicant_education = models.CharField(max_length=30)
    salary_expectations = models.CharField(max_length=30)
    applicant_experiences = models.TextField()
    compatibility = models.IntegerField()
    applied_date = models.DateTimeField(auto_now_add=True)

    @property
    def job_title(self):
        return self.job.title

    @property
    def applicant_name(self):
        return str(self.applicant_profile)

    @property
    def applicant_email(self):
        return str(self.applicant_profile.user)

    def save(self, *args, **kwargs):
        self.compatibility = self.calculate_compatibility()
        super().save(*args, **kwargs)

    def calculate_compatibility(self):
        score = 0
        if is_salary_compatible(self.salary_expectations, self.job.salary):
            score += 1
        if is_education_compatible(self.applicant_education,
                                   self.job.minimum_education):
            score += 1
        return score

    class Meta:
        unique_together = ['job', 'applicant_profile']
