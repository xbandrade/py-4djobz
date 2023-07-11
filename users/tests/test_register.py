from django.test import TestCase
from django.urls import resolve, reverse

from users import views


class ApplicantRegisterViewTest(TestCase):
    def test_users_register_view_is_correct(self):
        view = resolve(reverse('users:u_register'))
        self.assertIs(view.func.view_class, views.ApplicantRegisterView)

    def test_users_register_view_returns_status_200(self):
        response = self.client.get(reverse('users:u_register'))
        self.assertEqual(response.status_code, 200)

    def test_users_register_view_loads_correct_template(self):
        response = self.client.get(reverse('users:u_register'))
        self.assertTemplateUsed(
            response, 'users/pages/applicant_register.html')


class CompanyRegisterViewTest(TestCase):
    def test_users_register_view_is_correct(self):
        view = resolve(reverse('users:c_register'))
        self.assertIs(view.func.view_class, views.CompanyRegisterView)

    def test_users_register_view_returns_status_200(self):
        response = self.client.get(reverse('users:c_register'))
        self.assertEqual(response.status_code, 200)

    def test_users_register_view_loads_correct_template(self):
        response = self.client.get(reverse('users:c_register'))
        self.assertTemplateUsed(
            response, 'users/pages/company_register.html')
