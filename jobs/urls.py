from django.urls import path

from jobs import views

app_name = 'jobs'

urlpatterns = [
    path('list/',
         views.JobListView.as_view(), name='list'),
    path('publish/',
         views.JobPublishView.as_view(), name='publish'),
    path('update/<int:pk>/',
         views.JobUpdateView.as_view(), name='update'),
    path('search/',
         views.JobListViewSearch.as_view(), name='search'),
    path('j/<int:pk>/',
         views.JobDetailView.as_view(), name='job'),
    path('a/<int:pk>/',
         views.JobApplyView.as_view(), name='apply'),
    path('applicants/<int:pk>/',
         views.JobApplicantsView.as_view(), name='applicants'),
]
