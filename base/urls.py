from django.urls import path

from base import views

app_name = 'base'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
