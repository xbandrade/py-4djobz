from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from parameterized import parameterized

from users.forms import CompanyRegisterForm


class CompanyRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('name', 'Enter your company name'),
        ('email', 'Ex.: email@address.com'),
        ('password', 'Enter your password'),
        ('password2', 'Enter your password again'),
        ('phone_number', 'Ex.: 2499999999'),
        ('website', 'Ex.: https://www.company.com'),
        ('description', 'Enter your company description'),
    ])
    def test_company_register_fields_placeholder(self, field, placeholder):
        with translation.override('en'):
            form = CompanyRegisterForm()
            current = form[field].field.widget.attrs['placeholder']
            self.assertEqual(current, placeholder)

    @parameterized.expand([
        ('email',  'Enter a valid email'),
        ('password', (
            'Password must contain at least one uppercase character, '
            'one lowercase character and one number. The length should be '
            'at least 8 characters.'
        )),
    ])
    def test_company_register_fields_help_text(self, field, needed):
        with translation.override('en'):
            form = CompanyRegisterForm()
            current = form[field].field.help_text
            self.assertEqual(current, needed)

    @parameterized.expand([
        ('name', 'Company Name *'),
        ('email', 'Email *'),
        ('password', 'Password *'),
        ('password2', 'Repeat Password *'),
        ('phone_number', 'Phone Number'),
        ('website', 'Website'),
        ('description', 'Description'),
    ])
    def test_company_register_fields_label(self, field, needed):
        with translation.override('en'):
            form = CompanyRegisterForm()
            current = form[field].field.label
            self.assertEqual(current, needed)


class CompanyRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'name': 'My Company',
            'email': 'myemail@company.not',
            'password': 'Str0ngPa$$word',
            'password2': 'Str0ngPa$$word',
            'is_company': True,
        }

    @parameterized.expand([
        ('name', 'Company name cannot be empty'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please repeat your password'),
        ('email', 'Email is required'),
    ])
    def test_company_required_fields_cannot_be_empty(self, field, msg):
        msg = str(_(msg))
        self.form_data[field] = ''
        url = reverse('users:c_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_company_password_field_must_have_lower_upper_case_numbers(self):
        msg = str(_(
            'Password must contain at least an uppercase character, a '
            'lowercase character, a number and be at least 8 characters long.'
        ))
        self.form_data['password'] = '123q'
        url = reverse('users:c_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.form_data['password'] = '@ABC123qQ'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_company_password_and_password_confirmation_match(self):
        self.form_data['password'] = '@ABC123qQ'
        self.form_data['password2'] = '@ABCl23qD'
        url = reverse('users:c_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = str(_('Passwords must match'))
        self.assertIn(msg, response.context['form'].errors.get('password2'))
        self.assertIn(msg, response.content.decode('utf-8'))
        self.form_data['password'] = '@ABC123qQ'
        self.form_data['password2'] = '@ABC123qQ'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_company_get_request_to_registration_create_view_returns_404(self):
        url = reverse('users:c_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_company_email_field_must_be_unique(self):
        msg = str(_('User email is already in use'))
        url = reverse('users:c_create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_company_email_field_must_be_valid(self):
        msg = str(_('The email must be valid'))
        self.form_data['email'] = 'email'
        url = reverse('users:c_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_company_phone_number_cannot_contain_letters(self):
        msg = str(_('The phone number provided is invalid'))
        self.form_data['phone_number'] = '552423l5'
        url = reverse('users:c_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(
            msg, response.context['form'].errors.get('phone_number'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_applicant_dashboard_redirects_to_company_dashboard(self):
        url = reverse('users:c_create')
        self.client.post(url, data=self.form_data, follow=True)
        self.client.login(
            email='myemail@company.not', password='Str0ngPa$$word')
        url = reverse('users:u_dashboard')
        response = self.client.get(url, follow=True)
        self.assertRedirects(
            response, reverse('users:c_dashboard'))

    def test_company_not_authenticated_user_cannot_access_dashboard(self):
        url = reverse('users:c_dashboard')
        response = self.client.get(url, follow=True)
        self.assertRedirects(
            response, reverse('users:login') + '?next=' + url)

    def test_company_can_create_user_with_valid_form_data(self):
        with translation.override('en'):
            url = reverse('users:c_create')
            response = self.client.post(url, data=self.form_data, follow=True)
            self.assertRedirects(response, reverse('users:login'))
            self.assertIn(
                str(_('Company account has been created, please log in')),
                response.content.decode('utf-8')
            )


class CompanyLoginFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'name': 'My Company',
            'email': 'myemail@company.not',
            'password': 'Str0ngPa$$word',
            'password2': 'Str0ngPa$$word',
            'is_company': True,
        }

    def test_company_created_user_can_login(self):
        url = reverse('users:c_create')
        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            email='myemail@company.not', password='Str0ngPa$$word')
        self.assertTrue(is_authenticated)

    def test_company_get_request_to_logout_view_returns_404(self):
        url = reverse('users:logout')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)

    def test_company_cannot_log_another_user_out(self):
        with translation.override('en'):
            url = reverse('users:c_create')
            response = self.client.post(
                url, data=self.form_data, follow=True)
            self.client.login(
                email='myemail@company.not', password='Str0ngPa$$word')
            url = reverse('users:logout')
            response = self.client.post(
                url, data={'email': 'testcompany@test.not'}, follow=True)
            self.assertRedirects(response, reverse('base:home'))
            self.assertIn(str(_('Invalid logout user')),
                          response.content.decode('utf-8'))

    def test_company_user_can_logout_successfully(self):
        with translation.override('en'):
            url = reverse('users:c_create')
            response = self.client.post(url, data=self.form_data, follow=True)
            self.assertEqual(response.status_code, 200)
            self.client.login(
                email='myemail@company.not', password='Str0ngPa$$word')
            url = reverse('users:logout')
            response = self.client.post(
                url, data={'email': 'myemail@company.not'}, follow=True)
            self.assertRedirects(response, reverse('users:login'))
            self.assertIn(str(_('Logged out successfully')),
                          response.content.decode('utf-8'))

    def test_company_register_page_redirects_to_dashboard_if_logged_in(self):
        with translation.override('en'):
            url = reverse('users:c_create')
            response = self.client.post(url, data=self.form_data, follow=True)
            self.assertEqual(response.status_code, 200)
            self.client.login(
                email='myemail@company.not', password='Str0ngPa$$word')
            response = self.client.get(
                reverse('users:c_register'), follow=True)
            self.assertRedirects(response, reverse('users:c_dashboard'))
            self.assertIn(str(_('You cannot register while logged in')),
                          response.content.decode('utf-8'))
