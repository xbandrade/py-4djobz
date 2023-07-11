from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from users.forms import ApplicantRegisterForm
from users.models import ApplicantProfile


class ApplicantRegisterView(View):
    template_name = 'users/pages/applicant_register.html'

    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, _('You cannot register while logged in'))
            return redirect(reverse('users:u_dashboard'))
        form_data = request.session.pop('register_form_data', None)
        form = ApplicantRegisterForm(form_data)
        context = {
            'form': form,
            'form_action': reverse('users:u_create'),
        }
        return render(
            request, self.template_name, context=context
        )


class ApplicantCreateView(View):
    def get(self, request):
        raise Http404()

    def post(self, request):
        POST = request.POST
        request.session['register_form_data'] = POST
        form = ApplicantRegisterForm(POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            ApplicantProfile.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name', ''),
                last_name=form.cleaned_data.get('last_name', ''),
                title=form.cleaned_data.get('title', ''),
                years_experience=form.cleaned_data.get('years_experience', 0),
                experience=form.cleaned_data.get('experience', ''),
                education=form.cleaned_data.get('education', ''),
                skills=form.cleaned_data.get('skills', ''),
            )
            user_created = _(
                'User has been created, please log in'
            )
            messages.success(request, user_created)
            del request.session['register_form_data']
            return redirect(reverse('users:login'))
        return redirect('users:u_register')
