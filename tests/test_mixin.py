from django.urls import reverse

from jobs.models import Application, Job
from users.models import ApplicantProfile, CompanyProfile, CustomUser


class JobMixin:
    def make_applicant(self, years_experience=5):
        applicant_user = CustomUser.objects.create(
            email='applicant@example.com',
            password='StrongP@ssw0rd',
            phone_number=123456789,
            is_company=False,
            is_staff=False,
            is_superuser=False,
        )
        applicant_profile = ApplicantProfile.objects.create(
            user=applicant_user,
            first_name='First',
            last_name='Last',
            title='Software Developer',
            years_experience=years_experience,
            experience='Experience details...',
            education='Education details...',
            skills='Python, Django',
        )
        return {
            'applicant_user': applicant_user,
            'applicant_profile': applicant_profile,
        }

    def make_company(self):
        company_user = CustomUser.objects.create(
            email='company@example.com',
            phone_number=987654321,
            is_company=True,
            is_staff=False,
            is_superuser=False,
        )
        company_profile = CompanyProfile.objects.create(
            user=company_user,
            name='ABCompany',
            description='Company description...',
            website='https://www.company.com',
        )
        return {
            'company_user': company_user,
            'company_profile': company_profile,
        }

    def make_job(self, company_profile=None, is_finished=False,
                 title='Software Engineer', salary='> $3000'):
        if not company_profile:
            company_profile = self.make_company()['company_profile']
        return {
            'company_profile': company_profile,
            'job': Job.objects.create(
                company_profile=company_profile,
                title=title,
                salary=salary,
                skill_requirements='Python, Django',
                minimum_education="MBA/Master's degree",
                hide_salary=False,
                is_finished=is_finished,
            )
        }

    def make_all(self):
        applicant = self.make_applicant()
        company = self.make_company()
        job = self.make_job(company['company_profile'])
        return {
            'applicant_user': applicant['applicant_user'],
            'applicant_profile': applicant['applicant_profile'],
            'company_user': company['company_user'],
            'company_profile': company['company_profile'],
            'job': job['job']
        }

    def make_application(self, applicant=None, job=None):
        if not applicant:
            applicant = self.make_applicant()
        if not job:
            job = self.make_job()['job']
        return {
            'applicant_profile': applicant['applicant_profile'],
            'job': job,
            'application': Application.objects.create(
                job=job,
                applicant_profile=applicant['applicant_profile'],
                applicant_education="MBA/Master's degree",
                salary_expectations='> $3000'
            )
        }

    def login_as_applicant(self):
        self.form_data = {
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'myemail@email.not',
            'password': 'Str0ngPa$$word',
            'password2': 'Str0ngPa$$word',
            'is_company': False,
        }
        self.client.post(
            reverse('users:u_create'), data=self.form_data, follow=True)
        self.client.login(email='myemail@email.not', password='Str0ngPa$$word')

    def login_as_company(self):
        self.form_data = {
            'name': 'First',
            'email': 'myemail@email.not',
            'password': 'Str0ngPa$$word',
            'password2': 'Str0ngPa$$word',
            'is_company': True,
        }
        self.client.post(
            reverse('users:c_create'), data=self.form_data, follow=True)
        self.client.login(email='myemail@email.not', password='Str0ngPa$$word')
