from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from tests import JobMixin


class JobListViewSearchTest(TestCase, JobMixin):
    def setUp(self) -> None:
        job_data = self.make_job(title='Software Engineer')
        company = job_data['company_profile']
        self.make_job(title='Software Developer', company_profile=company)
        self.make_job(title='Data Analyst', company_profile=company)
        self.make_job(
            title='Project Manager', company_profile=company, is_finished=True)

    def test_job_search_with_search_term_retrieves_correct_jobs(self):
        response = self.client.get(reverse('jobs:search'), {'q': 'Engineer'})
        queryset = response.context['jobs']
        self.assertEqual(len(queryset), 1)
        response = self.client.get(reverse('jobs:search'), {'q': 'Software'})
        queryset = response.context['jobs']
        self.assertEqual(len(queryset), 2)

    def test_job_search_with_empty_search_term_retrieves_all_open_jobs(self):
        response = self.client.get(reverse('jobs:search'), {'q': ''})
        queryset = response.context['jobs']
        self.assertEqual(len(queryset), 3)

    def test_job_search_will_not_retrieve_finished_jobs(self):
        response = self.client.get(reverse('jobs:search'), {'q': 'Manager'})
        queryset = response.context['jobs']
        self.assertEqual(len(queryset), 0)

    def test_job_search_page_title_is_correct(self):
        response = self.client.get(
            reverse('jobs:search'), {'q': 'Engineer'})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn(str(_('&quot;Engineer&quot')), content)
