from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from jobs import views
from tests import JobMixin


class JobListViewTest(TestCase, JobMixin):
    def test_jobs_list_view_is_correct(self):
        view = resolve(reverse('jobs:list'))
        self.assertIs(view.func.view_class, views.JobListView)

    def test_jobs_list_view_returns_status_200(self):
        response = self.client.get(reverse('jobs:list'))
        self.assertEqual(response.status_code, 200)

    def test_jobs_list_view_loads_correct_template(self):
        response = self.client.get(reverse('jobs:list'))
        self.assertTemplateUsed(response, 'jobs/pages/list.html')

    def test_jobs_list_view_shows_no_jobs_found_if_no_jobs(self):
        with translation.override('en'):
            response = self.client.get(reverse('jobs:list'))
            self.assertIn(
                str(_('No jobs found')), response.content.decode('utf-8'))

    def test_jobs_list_view_shows_jobs_if_there_are_jobs(self):
        with translation.override('en'):
            self.make_job()
            response = self.client.get(reverse('jobs:list'))
            self.assertNotIn(
                str(_('No jobs found')), response.content.decode('utf-8'))
            content = response.content.decode('utf-8')
            response_context_jobs = response.context['jobs']
            self.assertIn(str(_('Job Title')), content)
            self.assertEqual(len(response_context_jobs), 1)

    def test_jobs_list_view_doesnt_show_unpublished_jobs(self):
        with translation.override('en'):
            self.make_job(is_finished=True)
            response = self.client.get(reverse('jobs:list'))
            self.assertIn(
                str(_('No jobs found')), response.content.decode('utf-8'))
            response_context_jobs = response.context['jobs']
            self.assertEqual(len(response_context_jobs), 0)
