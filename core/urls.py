# core/urls.py
from django.urls import path
from . import views


app_name = 'core'  # Set app_name attribute

urlpatterns = [
    # URL patterns for core app
    path('', views.upload_form, name='upload_form'),
    path('list/', views.list_files, name='list-view'),
]