from django.test import TestCase
from django.urls import resolve, reverse

from jobs import views
from tests import JobMixin


class JobDetailViewTest(TestCase, JobMixin):
    def setUp(self) -> None:
        self.data = self.make_all()
        self.job = self.data['job']
        self.applicant = self.data['applicant_user']
        self.company = self.data['company_user']
        self.company_profile = self.data['company_profile']

    def test_job_detail_view_is_correct(self):
        view = resolve(reverse('jobs:job', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.JobDetailView)

    def test_job_detail_view_returns_404_if_job_not_found(self):
        response = self.client.get(
            reverse('jobs:job', kwargs={'pk': 9999})
        )
        self.assertEqual(response.status_code, 404)

    def test_job_detail_template_doesnt_load_unpublished_recipe(self):
        new_job = self.make_job(self.company_profile, is_finished=True)['job']
        response = self.client.get(
            reverse('jobs:job', kwargs={'pk': new_job.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_job_detail_template_loads_correct_job(self):
        job_title = 'Python Developer'
        job = self.make_job(self.company_profile, title=job_title)['job']
        response = self.client.get(
            reverse('jobs:job', kwargs={'pk': job.id}))
        content = response.content.decode('utf-8')
        self.assertIn(job_title, content)

    def test_job_detail_view_returns_404_if_job_is_finished(self):
        job_data = self.make_job(self.company_profile, is_finished=True)
        job_id = job_data['job'].id
        response = self.client.get(
            reverse('jobs:job', kwargs={'pk': job_id})
        )
        self.assertEqual(response.status_code, 404)
