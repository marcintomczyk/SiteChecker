from django.urls import path

from . import views

app_name = 'site_checker'
urlpatterns = [
    # ex: /site-checker/
    path('', views.index, name='index'),
    # ex: /site-checker/check/
    path('check/', views.check, name='check'),
]