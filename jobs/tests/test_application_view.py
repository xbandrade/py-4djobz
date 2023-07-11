from django.test import TestCase
from django.urls import resolve, reverse

from jobs import views
from tests import JobMixin


class JobApplicationViewTest(TestCase, JobMixin):
    def setUp(self) -> None:
        self.data = self.make_all()
        self.job = self.data['job']
        self.applicant = self.data['applicant_user']
        self.company = self.data['company_user']
        self.company_profile = self.data['company_profile']

    def test_job_application_view_is_correct(self):
        view = resolve(reverse('jobs:apply', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.JobApplyView)

    def test_user_cannot_apply_if_not_authenticated(self):
        url = reverse('jobs:apply', kwargs={'pk': 1})
        response = self.client.get(url, follow=True)
        self.assertTemplateNotUsed(response, 'jobs/pages/apply.html')
        self.assertRedirects(response, reverse('users:login') + '?next=' + url)

    def test_job_application_view_returns_404_if_job_not_found(self):
        self.login_as_applicant()
        response = self.client.get(
            reverse('jobs:apply', kwargs={'pk': 9999}), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_job_application_view_returns_404_if_job_is_finished(self):
        self.login_as_applicant()
        job_data = self.make_job(self.company_profile, is_finished=True)
        job_id = job_data['job'].id
        response = self.client.get(
            reverse('jobs:apply', kwargs={'pk': job_id}), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_company_cannot_apply_to_a_job(self):
        self.login_as_company()
        url = reverse('jobs:apply', kwargs={'pk': 1})
        response = self.client.get(url, follow=True)
        self.assertTemplateNotUsed(response, 'jobs/pages/apply.html')
        self.assertEqual(response.status_code, 404)
