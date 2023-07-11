from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from parameterized import parameterized

from users.forms import ApplicantRegisterForm


class ApplicantRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Enter your first name'),
        ('last_name', 'Enter your last name'),
        ('email', 'Ex.: email@address.com'),
        ('phone_number', 'Ex.: 2499999999'),
        ('password', 'Enter your password'),
        ('password2', 'Enter your password again'),
        ('title', 'Enter your professional title'),
        ('years_experience', 'Ex.: 4'),
        ('education', 'Your academic education'),
        ('experience', 'Your previous professional experience'),
        ('skills', 'Your best skills')
    ])
    def test_applicant_register_fields_placeholder(self, field, placeholder):
        with translation.override('en'):
            form = ApplicantRegisterForm()
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
    def test_applicant_register_fields_help_text(self, field, needed):
        with translation.override('en'):
            form = ApplicantRegisterForm()
            current = form[field].field.help_text
            self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'First Name *'),
        ('last_name', 'Last Name *'),
        ('email', 'Email *'),
        ('password', 'Password *'),
        ('password2', 'Repeat Password *'),
        ('phone_number', 'Phone Number'),
        ('title', 'Title'),
        ('years_experience', 'Years of Experience'),
        ('education', 'Education'),
        ('experience', 'Previous Experience'),
        ('skills', 'Skills')
    ])
    def test_applicant_register_fields_label(self, field, needed):
        with translation.override('en'):
            form = ApplicantRegisterForm()
            current = form[field].field.label
            self.assertEqual(current, needed)


class ApplicationRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'myemail@email.not',
            'password': 'Str0ngPa$$word',
            'password2': 'Str0ngPa$$word',
            'is_company': False,
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('first_name', 'First name cannot be empty'),
        ('last_name', 'Last name cannot be empty'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please repeat your password'),
        ('email', 'Email is required'),
    ])
    def test_applicant_required_fields_cannot_be_empty(self, field, message):
        self.form_data[field] = ''
        url = reverse('users:u_create')
        msg = str(_(message))
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_applicant_password_field_must_have_lower_upper_case_numbers(self):
        msg = str(_(
            'Password must contain at least an uppercase character, a '
            'lowercase character, a number and be at least 8 characters long.'
        ))
        self.form_data['password'] = '123q'
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.form_data['password'] = '@ABC123qQ'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_applicant_password_and_password_confirmation_match(self):
        self.form_data['password'] = '@ABC123qQ'
        self.form_data['password2'] = '@ABCl23qD'
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = str(_('Passwords must match'))
        self.assertIn(msg, response.context['form'].errors.get('password2'))
        self.assertIn(msg, response.content.decode('utf-8'))
        self.form_data['password'] = '@ABC123qQ'
        self.form_data['password2'] = '@ABC123qQ'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_applicant_get_request_to_registration_view_returns_404(self):
        url = reverse('users:u_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_applicant_email_field_must_be_unique(self):
        msg = str(_('User email is already in use'))
        url = reverse('users:u_create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_applicant_email_field_must_be_valid(self):
        msg = str(_('The email must be valid'))
        self.form_data['email'] = 'email'
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_applicant_phone_number_cannot_contain_letters(self):
        msg = str(_('The phone number provided is invalid'))
        self.form_data['phone_number'] = '552423l5'
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(
            msg, response.context['form'].errors.get('phone_number'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_applicant_years_of_experience_must_be_an_integer(self):
        msg = str(_('Please enter a valid integer value'))
        self.form_data['years_experience'] = 'str'
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(
            msg, response.context['form'].errors.get('years_experience'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_applicant_years_of_experience_must_be_positive(self):
        msg = str(_('The years of experience provided is invalid'))
        self.form_data['years_experience'] = -1
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(
            msg, response.context['form'].errors.get('years_experience'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_applicant_years_of_experience_must_be_less_than_100(self):
        msg = str(_('The years of experience provided is invalid'))
        self.form_data['years_experience'] = 100
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(
            msg, response.context['form'].errors.get('years_experience'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_applicant_can_submit_with_valid_years_of_experience(self):
        self.form_data['years_experience'] = 8
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        form_errors = response.context['form'].errors.get('years_experience')
        self.assertIsNone(
            form_errors,
            f"Expected no errors in 'years_experience', but got {form_errors}"
        )

    def test_company_dashboard_redirects_to_applicant_dashboard(self):
        url = reverse('users:u_create')
        self.client.post(url, data=self.form_data, follow=True)
        self.client.login(
            email='myemail@email.not', password='Str0ngPa$$word')
        url = reverse('users:c_dashboard')
        response = self.client.get(url, follow=True)
        self.assertRedirects(
            response, reverse('users:u_dashboard'))

    def test_applicant_not_authenticated_user_cannot_access_dashboard(self):
        url = reverse('users:u_dashboard')
        response = self.client.get(url, follow=True)
        self.assertRedirects(
            response, reverse('users:login') + '?next=' + url)

    def test_applicant_can_create_user_with_valid_form_data(self):
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertRedirects(response, reverse('users:login'))
        self.assertIn(str(_('User has been created, please log in')),
                      response.content.decode('utf-8'))


class ApplicationLoginFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'myemail@email.not',
            'password': 'Str0ngPa$$word',
            'password2': 'Str0ngPa$$word',
            'is_company': False,
        }
        return super().setUp(*args, **kwargs)

    def test_applicant_created_user_can_login(self):
        url = reverse('users:u_create')
        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            email='myemail@email.not', password='Str0ngPa$$word')
        self.assertTrue(is_authenticated)

    def test_applicant_get_request_to_logout_view_returns_404(self):
        url = reverse('users:logout')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)

    def test_applicant_cannot_log_another_user_out(self):
        url = reverse('users:u_create')
        response = self.client.post(
            url, data=self.form_data, follow=True)
        self.client.login(
            email='myemail@email.not', password='Str0ngPa$$word')
        url = reverse('users:logout')
        response = self.client.post(
            url, data={'email': 'testuser@test.not'}, follow=True)
        self.assertRedirects(response, reverse('base:home'))
        self.assertIn(str(_('Invalid logout user')),
                      response.content.decode('utf-8'))

    def test_applicant_user_can_logout_successfully(self):
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.client.login(
            email='myemail@email.not', password='Str0ngPa$$word')
        url = reverse('users:logout')
        response = self.client.post(
            url, data={'email': 'myemail@email.not'}, follow=True)
        self.assertRedirects(response, reverse('users:login'))
        self.assertIn(str(_('Logged out successfully')),
                      response.content.decode('utf-8'))

    def test_applicant_register_page_redirects_to_dashboard_if_logged_in(self):
        url = reverse('users:u_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.client.login(
            email='myemail@email.not', password='Str0ngPa$$word')
        response = self.client.get(
            reverse('users:c_register'), follow=True)
        self.assertRedirects(response, reverse('users:u_dashboard'))
        self.assertIn(str(_('You cannot register while logged in')),
                      response.content.decode('utf-8'))
