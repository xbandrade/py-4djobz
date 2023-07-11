from django.forms import ValidationError
from django.test import TestCase

from tests.test_mixin import JobMixin


class CompanyModelTest(TestCase, JobMixin):
    def setUp(self) -> None:
        comp = self.make_company()
        self.company = comp['company_user']
        self.company_profile = comp['company_profile']

    def test_company_name_field_max_length_is_60(self):
        setattr(self.company_profile, 'name', 'a' * 61)
        with self.assertRaises(ValidationError):
            self.company_profile.full_clean()
