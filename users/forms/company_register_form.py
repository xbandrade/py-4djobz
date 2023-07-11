from string import ascii_letters as letters

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser
from utils import add_placeholder, strong_password


class CompanyRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['name'],
                        _('Enter your company name'))
        add_placeholder(self.fields['email'], _('Ex.: email@address.com'))
        add_placeholder(self.fields['password'], _('Enter your password'))
        add_placeholder(self.fields['password2'],
                        _('Enter your password again'))
        add_placeholder(self.fields['phone_number'], _('Ex.: 2499999999'))
        add_placeholder(self.fields['website'],
                        _('Ex.: https://www.company.com'))
        add_placeholder(self.fields['description'],
                        _('Enter your company description'))

    name = forms.CharField(
        error_messages={
            'required': _('Company name cannot be empty'),
        },
        required=True,
        label=_('Company Name *'),
    )
    email = forms.EmailField(
        error_messages={
            'required': _('Email is required'),
            'invalid': _('The email must be valid'),
        },
        required=True,
        label=_('Email *'),
        help_text=_('Enter a valid email'),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        help_text=_(
            'Password must contain at least one uppercase character, '
            'one lowercase character and one number. The length should be '
            'at least 8 characters.'
        ),
        error_messages={
            'required': _('Password must not be empty'),
        },
        validators=[strong_password],
        label=_('Password *'),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        validators=[strong_password],
        label=_('Repeat Password *'),
        error_messages={
            'required': _('Please repeat your password'),
        }
    )
    phone_number = forms.CharField(
        label=_('Phone Number'),
        required=False,
        error_messages={
            'invalid': _('The phone number provided is invalid'),
        }
    )
    website = forms.URLField(
        label=_('Website'),
        required=False
    )
    description = forms.CharField(
        label=_('Description'),
        widget=forms.Textarea,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'password2',
                  'phone_number', 'website', 'description']

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = CustomUser.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(
                _('User email is already in use'), code='unique'
            )
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', 0)
        if any(char in phone_number for char in letters):
            raise ValidationError(
                _('The phone number provided is invalid'), code='invalid'
            )
        return phone_number or 0

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            password_error = ValidationError(
                _('Passwords must match'),
                code='invalid',
            )
            raise ValidationError({
                'password2': [
                    password_error,
                ],
            })
        return cleaned_data
