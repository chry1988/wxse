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
    return HttpResponse('ok')


def closingMatters(request):
    return HttpResponse('ok2')
