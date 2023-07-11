from django.test import TestCase
from django.urls import resolve, reverse

from users import views


class UsersLoginViewTest(TestCase):
    def test_users_login_view_is_correct(self):
        view = resolve(reverse('users:login'))
        self.assertIs(view.func.view_class, views.LoginView)

    def test_users_login_view_returns_status_200(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_users_login_view_loads_correct_template(self):
        response = self.client.get(reverse('users:login'))
        self.assertTemplateUsed(response, 'users/pages/login.html')

    def test_users_get_request_to_login_create_view_returns_404(self):
        response = self.client.get(reverse('users:login_create'), follow=True)
        self.assertEqual(response.status_code, 404)
