from string import ascii_letters as letters

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser
from utils import add_placeholder, strong_password


class ApplicantRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], _('Enter your first name'))
        add_placeholder(self.fields['last_name'], _('Enter your last name'))
        add_placeholder(self.fields['email'], _('Ex.: email@address.com'))
        add_placeholder(self.fields['phone_number'], _('Ex.: 2499999999'))
        add_placeholder(self.fields['password'], _('Enter your password'))
        add_placeholder(self.fields['password2'],
                        _('Enter your password again'))
        add_placeholder(self.fields['title'],
                        _('Enter your professional title'))
        add_placeholder(self.fields['years_experience'],
                        _('Ex.: 4'))
        add_placeholder(self.fields['education'],
                        _('Your academic education'))
        add_placeholder(self.fields['experience'],
                        _('Your previous professional experience'))
        add_placeholder(self.fields['skills'],
                        _('Your best skills'))

    first_name = forms.CharField(
        error_messages={
            'required': _('First name cannot be empty'),
        },
        required=True,
        label=_('First Name *'),
    )
    last_name = forms.CharField(
        error_messages={
            'required': _('Last name cannot be empty'),
        },
        required=True,
        label=_('Last Name *'),
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
    phone_number = forms.CharField(
        label=_('Phone Number'),
        required=False,
        error_messages={
            'invalid': _('The phone number provided is invalid'),
        }
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
    title = forms.CharField(
        label=_('Title'),
        max_length=60,
        required=False
    )
    years_experience = forms.IntegerField(
        label=_('Years of Experience'),
        required=False,
        error_messages={
            'invalid': _('Please enter a valid integer value'),
        }
    )
    education = forms.CharField(
        label=_('Education'),
        widget=forms.Textarea,
        required=False
    )
    experience = forms.CharField(
        label=_('Previous Experience'),
        widget=forms.Textarea,
        required=False
    )
    skills = forms.CharField(
        label=_('Skills'),
        widget=forms.Textarea,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'password', 'password2', 'title',
                  'years_experience', 'skills', 'education', 'experience']

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

    def clean_years_experience(self):
        years_experience = self.cleaned_data.get('years_experience', 0)
        try:
            if not years_experience:
                return 0
            years_experience = int(years_experience)
            if years_experience < 0 or years_experience >= 100:
                raise ValueError
        except ValueError:
            raise ValidationError(
                _('The years of experience provided is invalid'),
                code='invalid'
            )
        return years_experience

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if not first_name:
            self.add_error('first_name', _('This field is required'))
        if not last_name:
            self.add_error('last_name', _('This field is required'))
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
