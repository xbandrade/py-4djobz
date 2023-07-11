from django.shortcuts import render

from .base_view import BaseView


class RegisterView(BaseView):
    template_name = 'global/pages/register.html'

    def get(self, request):
        context = self.get_context_data()
        return render(
            self.request,
            self.template_name,
            context
        )
