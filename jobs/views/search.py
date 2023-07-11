from django.db.models import Count, Q
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from jobs.models import Job


class JobListView(ListView):
    model = Job
    context_object_name = 'jobs'
    paginate_by = None
    ordering = ['-id']
    template_name = 'jobs/pages/list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_finished=False)
        queryset = queryset.select_related('company_profile')
        queryset = queryset.annotate(application_count=Count('applications'))
        return queryset


class JobListViewSearch(JobListView):
    template_name = 'jobs/pages/list.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            Q(title__icontains=search_term),
            is_finished=False,
        ).order_by('-id')
        return queryset

    def get_context_data(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        queryset = self.get_queryset(*args, **kwargs)

        if search_term:
            queryset = queryset.filter(Q(title__icontains=search_term))

        ctx = super().get_context_data(*args, **kwargs)
        search_translation = _('Searching for')

        ctx.update({
            'page_title': f'{search_translation} "{search_term}"',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
            'jobs': queryset,
        })
        return ctx


class JobDetailView(DetailView):
    model = Job
    context_object_name = 'job'
    template_name = 'jobs/pages/detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True
        })
        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_finished=False)
        if not qs:
            raise Http404()
        return qs
