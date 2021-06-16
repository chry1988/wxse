from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('myworkbench', views.myWorkBench),
    path('todomatters', views.toDoMatters),
    path('todomattersdetail', views.toDoMattersDetail),
    path('finishmatters', views.finishMatters),
    path('closingmatters', views.closingMatters),
    path('vulnerabilitydetailview', views.vulnerabilityDetailView),
    path('scheduledetailview', views.scheduleDetailView),
    path('warningnotice', views.warningNotice),
    path('warningnotice/add', views.warningNoticeAdd),
    path('warningnoticedetail', views.warningNoticeDetail),
    path('releasematters', views.releaseMatters),
    path('releasematters/change', views.releaseMatters),
    path('releasematters/check', views.releaseMatters),
    path('releasematters/getdetail', views.releaseMatters),
    path('releasematters/release', views.releaseMatters),
    path('releasematters/delete', views.releaseMatters),
    path('checkmatters', views.checkMatters),
    path('checkmatters/getdetail', views.checkMatters),
    path('checkmatters/pass', views.checkMatters),
    path('checkmatters/sendback', views.checkMatters),

]
