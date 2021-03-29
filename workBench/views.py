from django.shortcuts import render, HttpResponse
from configureDataBase.models.workBench import *


# Create your views here.
def myWorkBench(request):
    '''
    :param request:
    :return:
    '''
    # request.user
    result = userScheduleControler.objects.all()
    upcomingTasks = 1
    finishTasks = 0
    return render(request, 'workBench/myWorkBench.html', {'upcomingTasks': upcomingTasks, 'finishTasks': finishTasks})


def toDoMatters(request):
    return render(request, 'workBench/toDoMatters.html', )


def finishMatters(request):
    return render(request, 'workBench/finishMatters.html', )


def closingMatters(request):
    return render(request, 'workBench/closingMatters.html', )


def vulnerabilityDetailView(request):
    return None


def scheduleDetailView(request):
    return None


def warningNotice(request):
    return render(request, 'workBench/warningNotice.html', )


def warningNoticeDetail(request):
    return None
