from django.shortcuts import render, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.db.models import Count
import json
from configureDataBase.models.workBench import *
from configureDataBase.models.vulnerabilityControler import *
from configureDataBase.models.warningNotice import *


# Create your views here.
def myWorkBench(request):
    '''
    :param request:
    :return:
    '''
    targetUser = request.user.id
    upComingTasks = userScheduleControler.objects.filter(taskUser=targetUser, status='已下发').count()
    if upComingTasks == 0:
        upComingTasks = '目前没有代办任务'
    else:
        upComingTasks = '目前有' + str(upComingTasks) + '代办任务'
    finishTasks = userScheduleControler.objects.filter(taskUser=targetUser, status='已完成').count()
    return render(request, 'workBench/myWorkBench.html', {'upcomingTasks': upComingTasks, 'finishTasks': finishTasks})


def toDoMatters(request):
    targetUser = request.user.id
    toDoTasks = userScheduleControler.objects.filter(taskUser=targetUser, status='已下发')
    return render(request, 'workBench/toDoMatters.html', {'toDoTasks': toDoTasks, })


def toDoMattersDetail(request):
    if request.method == 'GET':
        searchId = request.GET.get('tid')
        targetUser = request.user.id
        queryResult = vulnerability.objects.filter(userschedulecontroler__id=searchId).values(
            'name',
            'detail',
            'level',
            'repair_method',
            'cve_num',
            'cnnvd_num',
            'dtime',
        )
        result = json.dumps({'queryResult': list(queryResult)}, cls=DjangoJSONEncoder)
        return HttpResponse(result)
    else:
        return None


def finishMatters(request):
    targetUser = request.user.id
    finishTasks = userScheduleControler.objects.filter(taskUser=targetUser, status='已修复')
    return render(request, 'workBench/finishMatters.html', {'finishTasks': finishTasks, })


def closingMatters(request):
    targetUser = request.user.id
    closingTasks = userScheduleControler.objects.filter(taskUser=targetUser, status='已完成')
    return render(request, 'workBench/closingMatters.html', {'closingTasks': closingTasks})


def vulnerabilityDetailView(request):
    vulnerabilityDetailResult = vulnerability.objects.get()
    return None


def scheduleDetailView(request):
    return None


def warningNotice(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    return render(request, 'workBench/warningNotice.html', )


def warningNoticeDetail(request):

    return None
