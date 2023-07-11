from django.test import TestCase
from django.urls import resolve, reverse

from base import views


class BaseRegisterViewTest(TestCase):
    def test_base_register_view_is_correct(self):
        view = resolve(reverse('base:register'))
        self.assertIs(view.func.view_class, views.RegisterView)

    def test_base_register_view_returns_status_200(self):
        response = self.client.get(reverse('base:register'))
        self.assertEqual(response.status_code, 200)

    def test_base_register_view_loads_correct_template(self):
        response = self.client.get(reverse('base:register'))
        self.assertTemplateUsed(response, 'global/pages/register.html')
