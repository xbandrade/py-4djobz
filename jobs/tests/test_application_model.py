from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

from tests import JobMixin


class ApplicationModelTest(TestCase, JobMixin):
    def setUp(self) -> None:
        app = self.make_application()
        self.application = app['application']
        self.job = app['job']

    @parameterized.expand([
        ('applicant_education', 15),
        ('salary_expectations', 15),
    ])
    def test_application_fields_max_length(self, field, max_length):
        setattr(self.application, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.application.full_clean()
