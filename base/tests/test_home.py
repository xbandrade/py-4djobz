from django.test import TestCase
from django.urls import resolve, reverse

from base import views


class BaseHomeViewTest(TestCase):
    def test_the_test(self):
        assert 1

    def test_base_home_view_is_correct(self):
        view = resolve(reverse('base:home'))
        self.assertIs(view.func.view_class, views.HomeView)

    def test_base_home_view_returns_status_200(self):
        response = self.client.get(reverse('base:home'))
        self.assertEqual(response.status_code, 200)

    def test_base_home_view_loads_correct_template(self):
        response = self.client.get(reverse('base:home'))
        self.assertTemplateUsed(response, 'global/pages/home.html')
