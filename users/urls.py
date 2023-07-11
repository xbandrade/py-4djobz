from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/',
         views.LoginView.as_view(), name='login'),
    path('logincreate/',
         views.LoginCreateView.as_view(), name='login_create'),
    path('u/register/',
         views.ApplicantRegisterView.as_view(), name='u_register'),
    path('u/create/',
         views.ApplicantCreateView.as_view(), name='u_create'),
    path('u/dashboard/',
         views.ApplicantDashboardView.as_view(), name='u_dashboard'),
    path('c/register/',
         views.CompanyRegisterView.as_view(), name='c_register'),
    path('c/create/',
         views.CompanyCreateView.as_view(), name='c_create'),
    path('c/dashboard/',
         views.CompanyDashboardView.as_view(), name='c_dashboard'),
    path('c/delete/', views.DashboardJobDelete.as_view(),
         name='job_delete'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('c/charts/',
         views.CompanyChartsView.as_view(), name='charts'),
]
