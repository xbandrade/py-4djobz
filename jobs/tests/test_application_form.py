from django.db.utils import IntegrityError
from django.test import TestCase

from tests import JobMixin


class ApplicationFormTest(TestCase, JobMixin):
    def setUp(self) -> None:
        self.data = self.make_all()
        self.job = self.data['job']
        self.applicant = self.data['applicant_user']
        self.applicant_profile = self.data['applicant_profile']
        self.company = self.data['company_user']
        self.company_profile = self.data['company_profile']

    def test_applicant_cannot_apply_to_the_same_job_twice(self):
        with self.assertRaises(IntegrityError):
            self.make_application(self.data, self.job)
            self.make_application(self.data, self.job)
