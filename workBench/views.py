from django.shortcuts import render, HttpResponse
from django.db.models import Q
from django.db.models import Count
from configureDataBase.models.workBench import *
from configureDataBase.models.vulnerabilityControler import *


# Create your views here.
def myWorkBench(request):
    '''
    :param request:
    :return:
    '''
    targetUser = request.user.id
    result = userScheduleControler.objects.all()
    upcomingTasks = userScheduleControler.objects.aggregate(taskUser=targetUser, status=0)
    finishTasks = userScheduleControler.objects.aggregate(taskUser=targetUser, status=1)
    return render(request, 'workBench/myWorkBench.html', {'upcomingTasks': upcomingTasks, 'finishTasks': finishTasks})


def toDoMatters(request):
    targetUser = request.user.id
    toDoTasks = userScheduleControler.objects.filter(taskUser=targetUser, status=0)
    return render(request, 'workBench/toDoMatters.html', {'toDoTasks': toDoTasks, })


def finishMatters(request):
    targetUser = request.user.id
    finishTasks = userScheduleControler.objects.filter(taskUser=targetUser, status=0)
    return render(request, 'workBench/finishMatters.html', {'finishTasks': finishTasks, })


def closingMatters(request):
    targetUser = request.user.id
    closingTasks = userScheduleControler.objects.filter(taskUser=targetUser, status=0)
    return render(request, 'workBench/closingMatters.html', {'closingTasks': closingTasks})


def vulnerabilityDetailView(request):
    vulnerabilityDetailResult = vulnerability.objects.get()
    return None


def scheduleDetailView(request):
    return None


def warningNotice(request):
    return render(request, 'workBench/warningNotice.html', )


def warningNoticeDetail(request):
    return None
