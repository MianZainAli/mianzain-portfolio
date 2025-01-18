from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    path('projects/', views.Projects, name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetail, name='project-details'),
    path('contact/submit/', views.contact_submit, name='contact-submit'),
]
