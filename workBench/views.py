from django.shortcuts import render, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_protect
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
    upComingTasks = userScheduleControler.objects.filter(taskUser=targetUser, status=2).count()
    if upComingTasks == 0:
        upComingTasks = '目前没有代办任务'
    else:
        upComingTasks = '目前有' + str(upComingTasks) + '代办任务'
    finishTasks = userScheduleControler.objects.filter(taskUser=targetUser, status=7).count()
    return render(request, 'workBench/myWorkBench.html', {'upcomingTasks': upComingTasks, 'finishTasks': finishTasks})


# @csrf_protect
def toDoMatters(request):
    if request.method == 'GET':
        targetUser = request.user.id

        toDoTasks = userScheduleControler.objects.filter(taskUser=targetUser, status=2).values(
            'id',
            'taskVulnerability__id',
            'taskVulnerability__name',
            'taskVulnerability__detail',
            'taskVulnerability__level',
            'taskVulnerability__repair_method',
            'taskVulnerability__cve_num',
            'taskVulnerability__cnnvd_num',
            'taskVulnerability__dtime',
            'taskVulnerability__professionalwork__workName',
            'taskAffectIP__ip'
        )
        print(toDoTasks)
        return render(request, 'workBench/toDoMatters.html', {'toDoTasks': toDoTasks, })
    elif request.method == 'POST':
        doAction = request.POST.get('action')
        userScheduleControlerID = request.POST.get('tid')
        targetUser = request.user.id
        doResult = userScheduleControler.objects.get(id=userScheduleControlerID)
        print(doResult.id)
        doAction = int(doAction)
        if doAction == 0:
            doResult.status = 4
            doResult.save()
        elif doAction == 1:
            doResult.status = 3
            doResult.save()
        return HttpResponse('success')


# @csrf_protect
def toDoMattersDetail(request):
    if request.method == 'GET':
        searchId = request.GET.get('tid')
        targetUser = request.user.id
        queryResult = vulnerability.objects.filter(userschedulecontroler=searchId).values(
            'name',
            'detail',
            'level',
            'repair_method',
            'cve_num',
            'cnnvd_num',
            'dtime',
        )
        queryIPResult = IpV4.objects.filter(userschedulecontroler=searchId).values(
            'ip',
            'area',
        )
        queryProfessionsalWrokResult = professionalWork.objects.filter(relationVulnerability=searchId).values(
            'workName',
            'priorityLevel',
        )
        result = json.dumps({'queryResult': list(queryResult), 'queryIPResult': list(queryIPResult),
                             'queryProfessionsalWrokResult': list(queryProfessionsalWrokResult)}, cls=DjangoJSONEncoder)
        return HttpResponse(result)
    elif request.method == 'POST':
        doAction = request.POST.get('action')
        userScheduleControlerID = request.POST.get('tid')
        targetUser = request.user.id
        doResult = userScheduleControler.objects.get(id=userScheduleControlerID)
        if doAction == 0:
            doResult.status = 4
            doResult.save()
        elif doAction == 1:
            doResult.status = 3
            doResult.save()
        return None


def finishMatters(request):
    targetUser = request.user.id

    finishTaskID = request.GET.get('tid')
    if finishTaskID:
        finishTasks = userScheduleControler.objects.filter(taskUser=targetUser, id=finishTaskID).values(
            'status',
        )
        statusProgress = {
            0: ['录入', '10%', '10'],
            1: ['已提交', '20%', '20'],
            2: ['已下发', '30%', '30'],
            3: ['已修复', '50%', '50'],
            4: ['暂缓修复', '40%', '40'],
            5: ['已校验', '80%', '80'],
            6: ['已办结', '90%', '90'],
            7: ['已完成', '100%', '100'],
        }
        statusProgressValue = statusProgress[finishTasks[0]['status']]
        print(statusProgressValue)
        result = json.dumps({'statusProgressValue': statusProgressValue, }, cls=DjangoJSONEncoder)
        return HttpResponse(result)
    else:
        finishTasks = userScheduleControler.objects.filter(taskUser=targetUser, status__gte=3).values(
            'id',
            'taskVulnerability__id',
            'taskVulnerability__name',
            'taskVulnerability__detail',
            'taskVulnerability__level',
            'taskVulnerability__repair_method',
            'taskVulnerability__cve_num',
            'taskVulnerability__cnnvd_num',
            'taskVulnerability__dtime',
            'taskVulnerability__professionalwork__workName',
            'taskAffectIP__ip'
        )

    return render(request, 'workBench/finishMatters.html', {'finishTasks': finishTasks, })


def closingMatters(request):
    targetUser = request.user.id
    closingTasks = userScheduleControler.objects.filter(taskUser=targetUser, status=7)
    return render(request, 'workBench/closingMatters.html', {'closingTasks': closingTasks})


def vulnerabilityDetailView(request):
    vulnerabilityDetailResult = vulnerability.objects.get()
    return None


def scheduleDetailView(request):
    return None


def warningNotice(request):
    if request.method == 'GET':
        warningNoticeResult = NoticeDetial.objects.all()
        return render(request, 'workBench/warningNotice.html', {'warningNoticeResult': warningNoticeResult, })
    elif request.method == 'POST':

        noticeName = models.CharField(max_length=255, verbose_name='通告名称')
        noticeDate = models.DateTimeField(verbose_name='通告时间')
        noyiceStaff = models.CharField(max_length=255, verbose_name='通告人员')
        noticeLevel = models.CharField(max_length=255, verbose_name='严重级别')
        CVEserialNumber = models.CharField(max_length=255, verbose_name='CVE编号')
        CNNVDserialNumber = models.CharField(max_length=255, verbose_name='CNNVD编号')
        affectedVendor = models.CharField(max_length=255, verbose_name='影响厂商')
        affectedComponent = models.CharField(max_length=255, verbose_name='影响组件')
        noticeDetail = models.TextField(verbose_name='通告描述')
    return render(request, 'workBench/warningNotice.html', )


def warningNoticeDetail(request):
    if request.method == 'GET':
        warningNoticeResult = NoticeDetial.objects.all()
        return render(request, 'workBench/warningNotice.html', {'warningNoticeResult': warningNoticeResult, })
    elif request.method == 'POST':

        noticeName = models.CharField(max_length=255, verbose_name='通告名称')
        noticeDate = models.DateTimeField(verbose_name='通告时间')
        noyiceStaff = models.CharField(max_length=255, verbose_name='通告人员')
        noticeLevel = models.CharField(max_length=255, verbose_name='严重级别')
        CVEserialNumber = models.CharField(max_length=255, verbose_name='CVE编号')
        CNNVDserialNumber = models.CharField(max_length=255, verbose_name='CNNVD编号')
        affectedVendor = models.CharField(max_length=255, verbose_name='影响厂商')
        affectedComponent = models.CharField(max_length=255, verbose_name='影响组件')
        noticeDetail = models.TextField(verbose_name='通告描述')
    return render(request, 'workBench/warningNotice.html', )
