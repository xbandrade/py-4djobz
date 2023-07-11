from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .base_view import BaseView


class AboutView(BaseView):
    template_name = 'global/pages/about.html'

    def get(self, request):
        context = self.get_context_data()
        about_text = [
            _('''This is 4Djobz!'''),
            _('''Want to find a new job opportunity or need to hire
              the perfect candidates?'''),
            _('''4Djobz is the right place!'''),
        ]
        context['about_text'] = about_text
        return render(
            self.request,
            self.template_name,
            context
        )
