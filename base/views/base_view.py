from django.views import View


class BaseView(View):
    template_name = ''

    def get_context_data(self):
        current_path = self.request.path
        context = {
            'curr_path': current_path,
        }
        return context
