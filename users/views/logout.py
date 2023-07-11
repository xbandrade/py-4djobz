from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        raise Http404()

    def post(self, request):
        if request.POST.get('email') != request.user.email:
            messages.error(request, _('Invalid logout user'))
        else:
            logout(request)
            messages.success(request, _('Logged out successfully'))
        return redirect(reverse('users:login'))
