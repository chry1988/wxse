from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('myworkbench', views.myWorkBench),
    path('todomatters', views.toDoMatters),
    path('closingmatters', views.closingMatters),
]
