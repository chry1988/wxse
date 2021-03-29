from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('myworkbench', views.myWorkBench),
    path('todomatters', views.toDoMatters),
    path('finishmatters', views.finishMatters),
    path('closingmatters', views.closingMatters),
    path('vulnerabilitydetailview', views.vulnerabilityDetailView),
    path('scheduledetailview', views.scheduleDetailView),
    path('warningnotice', views.warningNoticeDetail),
    path('warningnoticedetail', views.warningNoticeDetail),
]
