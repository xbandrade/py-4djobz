from django import forms
from django.utils.translation import gettext_lazy as _

from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['email'], _('Enter your email'))
        add_placeholder(self.fields['password'], _('Enter your password'))

    email = forms.CharField(label=_('Email *'))
    password = forms.CharField(
        widget=forms.PasswordInput(), label=_('Password *'))
