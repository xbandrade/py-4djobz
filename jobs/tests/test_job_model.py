from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

from tests import JobMixin


class JobModelTest(TestCase, JobMixin):
    def setUp(self) -> None:
        self.job = self.make_job()['job']

    @parameterized.expand([
        ('title', 100),
        ('salary', 30),
        ('minimum_education', 40),
    ])
    def test_job_fields_max_length(self, field, max_length):
        setattr(self.job, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.job.full_clean()

    def test_job_hide_salary_is_false_by_default(self):
        self.assertFalse(self.job.hide_salary)

    def test_job_is_finished_is_false_by_default(self):
        self.assertFalse(self.job.is_finished)

    def test_job_string_representation(self):
        job_title = 'New Job Title'
        self.job.title = job_title
        self.job.full_clean()
        self.job.save()
        self.assertEqual(str(self.job), job_title)
