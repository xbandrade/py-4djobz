from django.test import TestCase
from django.urls import resolve, reverse

from users import views


class UsersLogoutViewTest(TestCase):
    def test_users_logout_view_is_correct(self):
        view = resolve(reverse('users:logout'))
        self.assertIs(view.func.view_class, views.UserLogoutView)

    def test_get_request_to_logout_view_returns_404_status_code(self):
        response = self.client.get(reverse('users:logout'), follow=True)
        self.assertEqual(response.status_code, 404)
