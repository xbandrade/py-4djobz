from django.forms import ValidationError
from django.test import TestCase
from parameterized import parameterized

from tests.test_mixin import JobMixin


class ApplicantModelTest(TestCase, JobMixin):
    def setUp(self) -> None:
        app = self.make_applicant()
        self.applicant = app['applicant_user']
        self.applicant_profile = app['applicant_profile']

    @parameterized.expand([
        ('first_name', 30),
        ('last_name', 30),
        ('title', 60),
    ])
    def test_applicant_model_fields_max_length(self, field, max_length):
        setattr(self.applicant_profile, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.applicant_profile.full_clean()
