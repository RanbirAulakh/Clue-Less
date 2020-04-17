from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('help', views.help_page, name='help'),
    path('about', views.about_page, name='about'),
    path('statistic', views.statistic_page, name='statistic')
]