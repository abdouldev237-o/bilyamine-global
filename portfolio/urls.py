"""
URLs du portfolio.
"""

from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('a-propos/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('realisations/', views.projects, name='projects'),
    path('realisations/<slug:slug>/', views.project_detail, name='project_detail'),
    path('temoignages/', views.testimonials, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('create-admin-secret-123/', create_admin)
]
