from django.forms import ValidationError
from django.test import TestCase

from users.models import CustomUser


class CustomUserModelTest(TestCase):
    def test_custom_user_can_be_created_with_email_and_password(self):
        custom_user = CustomUser.objects.create_user(
            email='mycustomuser@email.com',
            password='StrongP@ssw0rd'
        )
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(custom_user.email, 'mycustomuser@email.com')
        self.assertEqual(custom_user.id, 1)

    def test_custom_user_cannot_be_created_with_no_email(self):
        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(
                email=None,
                password='StrongP@ssw0rd'
            )

    def test_custom_user_string_representation(self):
        email = 'mycustomuser@email.com'
        CustomUser.objects.create_user(
            email=email,
            password='StrongP@ssw0rd'
        )
        self.assertEqual(str(CustomUser.objects.get(email=email)), email)

    def test_create_superuser(self):
        email = 'admin@email.com'
        superuser = CustomUser.objects.create_superuser(
            email=email, password='StrongP@ssw0rd')
        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
