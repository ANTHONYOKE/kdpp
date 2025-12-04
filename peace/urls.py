
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('report/', views.report, name='report'),
    path('cases/', views.cases, name='cases'),
    path('contact/', views.contact, name='contact'),
]
