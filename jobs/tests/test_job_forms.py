from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from jobs.models import Job
from tests import JobMixin


class JobFormsTest(TestCase, JobMixin):
    def setUp(self):
        self.data = self.make_all()
        self.job = self.data['job']
        self.applicant_profile = self.data['applicant_profile']

    def test_job_can_be_created_successfully(self):
        with translation.override('en'):
            self.assertEqual(Job.objects.count(), 1)
            self.assertEqual(self.job.title, 'Software Engineer')
            self.assertEqual(self.job.salary, '> $3000')
            self.assertEqual(self.job.skill_requirements, 'Python, Django')
            self.assertEqual(self.job.minimum_education, "MBA/Master's degree")
            self.assertFalse(self.job.hide_salary)

    def test_company_name_property_works_properly(self):
        self.assertEqual(self.job.company_name, self.job.company_profile.name)

    def test_applicant_cannot_create_a_job_post(self):
        with self.assertRaises(ValueError):
            self.make_job(company_profile=self.applicant_profile)

    def test_company_can_create_a_job_post(self):
        self.make_job(company_profile=self.data['company_profile'])
        self.assertEqual(Job.objects.count(), 2)

    def test_applicant_gets_404_when_trying_to_publish_job(self):
        self.login_as_applicant()
        response = self.client.get(reverse('jobs:publish'), follow=True)
        self.assertTemplateNotUsed(response, 'jobs/pages/publish.html')
        self.assertEqual(response.status_code, 404)
