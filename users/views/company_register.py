from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from users.forms import CompanyRegisterForm
from users.models import CompanyProfile


class CompanyRegisterView(View):
    template_name = 'users/pages/company_register.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, _('You cannot register while logged in'))
            return redirect(reverse('users:c_dashboard'))
        form_data = request.session.pop('register_form_data', None)
        form = CompanyRegisterForm(form_data)
        context = {
            'form': form,
            'form_action': reverse('users:c_create'),
        }
        return render(
            request, self.template_name, context=context
        )


class CompanyCreateView(View):
    def get(self, request):
        raise Http404()

    def post(self, request):
        POST = request.POST
        request.session['register_form_data'] = POST
        form = CompanyRegisterForm(POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.is_company = True
            user.save()
            CompanyProfile.objects.create(
                user=user,
                name=form.cleaned_data.get('name', ''),
                website=form.cleaned_data.get('website', ''),
                description=form.cleaned_data.get('description', ''),
            )
            user_created = _(
                'Company account has been created, please log in'
            )
            messages.success(request, user_created)
            del request.session['register_form_data']
            return redirect(reverse('users:login'))
        return redirect('users:c_register')
