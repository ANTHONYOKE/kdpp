from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('report/', views.report_view, name='report'),  # updated view
    path('report/success/', views.report_success_view, name='report_success'),  # new success page
    path('cases/', views.cases, name='cases'),
    path('contact/', views.contact, name='contact'),
]
