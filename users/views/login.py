from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from users.forms import LoginForm


class LoginView(View):
    template_name = 'users/pages/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('base:home'))
        form = LoginForm()
        context = {
            'form': form,
            'form_action': reverse('users:login_create'),
        }
        return render(
            request, self.template_name, context=context)


class LoginCreateView(View):
    def get(self, request):
        raise Http404()

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            authenticated_user = authenticate(
                email=form.cleaned_data.get('email', ''),
                password=form.cleaned_data.get('password', ''),
            )
            if authenticated_user:
                messages.success(request, _('You are logged in'))
                login(request, authenticated_user)
            else:
                messages.error(request, _('Invalid email or password'))
                return redirect(reverse('users:login'))
        else:
            messages.error(request, _('Invalid credentials'))
            return redirect(reverse('users:login'))
        dashboard = (reverse('users:c_dashboard')
                     if authenticated_user.is_company
                     else reverse('users:u_dashboard'))
        return redirect(dashboard)
