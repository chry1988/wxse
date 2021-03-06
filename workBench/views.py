from django.shortcuts import render, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.db.models import Count
import json
from configureDataBase.models.workBench import *
from configureDataBase.models.vulnerabilityControler import *
from configureDataBase.models.warningNotice import *
from customUser.models import *
import re


# Create your views here.
def checkUserPrivileges(request, funRequest):
    checkUser = request.user.id
    checkPrivilege = wxseUser.objects.get(id=checkUser).userPrivilege
    if checkPrivilege == 0:
        return funRequest
    else:
        return HttpResponse('ban')


def adminUrls():
    pass


@login_required(login_url='/accounts/login')
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


@login_required(login_url='/accounts/login')
def releaseMatters(request):
    checkUser = request.user.id
    checkPrivilege = wxseUser.objects.get(id=checkUser).userPrivilege
    if checkPrivilege != 0:
        return HttpResponse('ban')
    if request.method == 'GET':

        userList = wxseUser.objects.all().values('id', 'first_name', 'last_name')

        waitToReleaseMatters = userScheduleControler.objects.filter(status=1).values(
            'id',
            'taskVulnerability__id',
            'taskVulnerability__name',
            'taskUser__first_name',
            'taskUser__last_name',
            'deadLine',
            # taskAffectIP = models.ManyToManyField(IpV4, default=None, blank=True)
            'affectedServie',
            'taskVulnerability__level'
        )
        waitToReleaseMattersPage = Paginator(waitToReleaseMatters, 20)
        if request.method == "GET":
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                waitToReleaseMattersPageObj = waitToReleaseMattersPage.page(page)
            except PageNotAnInteger:
                waitToReleaseMattersPageObj = waitToReleaseMattersPage.page(1)
            except InvalidPage:
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                waitToReleaseMattersPageObj = waitToReleaseMattersPage.page(waitToReleaseMattersPage.num_pages)
        return render(request, 'workBench/releaseMatters.html',
                      {'waitToReleaseMattersPage': waitToReleaseMattersPageObj, 'userList': userList})
    elif request.method == 'POST':
        modify = request.POST.get('modify')
        if modify == 'delete':
            tid = request.POST.get('tid')
            releaseMattersDelete = userScheduleControler.objects.get(id=tid)
            releaseMattersDelete.delete()
            result = json.dumps({'tid': tid})
            return HttpResponse(result)
        elif modify == 'release':
            tid = request.POST.get('tid')
            releaseMattersRelease = userScheduleControler.objects.get(id=tid)
            releaseMattersRelease.status = 2
            releaseMattersRelease.save()
            result = json.dumps({'tid': tid})
            return HttpResponse(result)
        elif modify == 'check':
            tid = request.POST.get('tid')
            releaseMattersCheck = userScheduleControler.objects.filter(id=tid).values(
                'status',
                'taskVulnerability__name',
                'taskVulnerability__dtime',
                'taskVulnerability__level',
                'taskVulnerability__detail',
                'taskVulnerability__cnnvd_num',
                'taskVulnerability__cve_num',
                'taskVulnerability__repair_method',
                'taskUser__first_name',
                'taskUser__last_name',
                'deadLine',
                'taskAffectIP',
                'affectedServie',
            )
            result = json.dumps({'queryresult': list(releaseMattersCheck), }, cls=DjangoJSONEncoder)
            return HttpResponse(result)

        vulnerabilityName = request.POST.get('vulnerabilityName')
        vulnerabilityDtime = request.POST.get('vulnerabilityDtime')
        CVEserialNumber = request.POST.get('CVEserialNumber')
        vulnerabilityDetail = request.POST.get('vulnerabilityDetail')
        vulnerabilityLevel = request.POST.get('vulnerabilityLevel')
        CNNVDserialNumber = request.POST.get('CNNVDserialNumber')
        vulnerabilityrepairMethod = request.POST.get('vulnerabilityrepairMethod')
        affectedServie = request.POST.get('affectedServie')
        uids = request.POST.get('uids')

        # django.db.utils.IntegrityError: UNIQUEconstraintfailed: configureDataBase_vulnerability.cve_num
        vulnerabilityObj = vulnerability.objects.create(
            name=vulnerabilityName,
            detail=vulnerabilityDetail,
            dtime=vulnerabilityDtime,
            repair_method=vulnerabilityrepairMethod,
            cve_num=CVEserialNumber,
            cnnvd_num=CNNVDserialNumber,
            level=vulnerabilityLevel,
        )
        # vulnerabilityObj=vulnerability.objects.get(id=vulnerabilityObj.id)
        userList = re.split(',', uids)
        userList = [i for i in userList if i != '']
        for uItem in userList:
            targetUser = wxseUser.objects.get(id=uItem)
            print(targetUser.email, )
            targetUserScheduleControler = userScheduleControler.objects.create(
                taskUser=targetUser,
                deadLine=vulnerabilityDtime,
                taskVulnerability=vulnerabilityObj,
                status=1,
                affectedServie=affectedServie,
            )

        return HttpResponse('ok')


@login_required(login_url='/accounts/login')
def checkMatters(request):
    if request.method == 'GET':
        modify = request.GET.get('modify')
        if modify == 'getdetail':
            tid = request.GET.get('tid')
            checkTasks = userScheduleControler.objects.filter(id=tid).values(
                'id',
                'status',
                'taskVulnerability__name',
                'taskUser__first_name',
                'deadLine',
                # 'taskAffectIP',
                'affectedServie',
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
            progressNoteObj = progressNote.objects.filter(userScheduleControlerNote=tid).values(
                'messageDetail',
                'messageDate',
                'messageAuthor',
            )
            statusProgressValue = statusProgress[checkTasks[0]['status']]
            result = json.dumps({'statusProgressValue': statusProgressValue, 'checkTask': checkTasks[0],
                                 'progressNoteObj': list(progressNoteObj)},
                                cls=DjangoJSONEncoder)
            return HttpResponse(result)
        else:
            checkMattersList = userScheduleControler.objects.all().values(
                'id',
                'taskVulnerability__id',
                'taskVulnerability__name',
                'affectedServie',
                'taskVulnerability__level',
                'status',
                'deadLine',
                'taskUser__first_name',
                'taskUser__last_name',
            )
            checkMattersListPage = Paginator(checkMattersList, 20)
            if request.method == "GET":
                page = request.GET.get('page')
                try:
                    checkMattersListObj = checkMattersListPage.page(page)
                except PageNotAnInteger:
                    checkMattersListObj = checkMattersListPage.page(1)
                except InvalidPage:
                    return HttpResponse('找不到页面的内容')
                except EmptyPage:
                    checkMattersListObj = checkMattersListPage.page(checkMattersListPage.num_pages)
            return render(request, 'workBench/checkMatters.html', {'checkMattersListPage': checkMattersListObj})

    elif request.method == 'POST':
        modify = request.POST.get('modify')
        if modify == 'pass':
            dtid = request.POST.get('dtid')
            checkMattersPass = userScheduleControler.objects.get(id=dtid)
            checkMattersPass.status = 5
            checkMattersPass.save()
            result = json.dumps({'dtid': dtid})
            return HttpResponse(result)
        elif modify == 'sendback':
            dtid = request.POST.get('dtid')
            checkMattersSendBack = userScheduleControler.objects.get(id=dtid)
            checkMattersSendBack.status = 2
            checkMattersSendBack.save()
            result = json.dumps({'dtid': dtid})
            return HttpResponse(result)


@login_required(login_url='/accounts/login')
def toDoMatters(request):
    if request.method == 'GET':
        targetUser = request.user.id
        page = request.GET.get('page')
        VulnerabilityId = request.GET.get('VulnerabilityId')
        VulnerabilityName = request.GET.get('VulnerabilityName')
        VulnerabilityAffectedServie = request.GET.get('VulnerabilityAffectedServie')
        VulnerabilityUser = request.GET.get('VulnerabilityUser')
        VulnerabilityLevel = request.GET.get('VulnerabilityLevel')
        if VulnerabilityId or VulnerabilityName or VulnerabilityAffectedServie or VulnerabilityUser or VulnerabilityLevel:
            print('success', VulnerabilityLevel, VulnerabilityId, VulnerabilityName, )
            toDoTasks = userScheduleControler.objects.filter(Q(taskUser=targetUser), Q(status=2),
                                                             Q(
                                                                 Q(taskVulnerability__name=VulnerabilityName) |
                                                                 Q(taskVulnerability__id=VulnerabilityId) |
                                                                 Q(affectedServie=VulnerabilityAffectedServie) |
                                                                 Q(taskVulnerability__level=VulnerabilityLevel)
                                                             )
                                                             ).values(
                'id',
                'taskVulnerability__id',
                'taskVulnerability__name',
                'taskVulnerability__detail',
                'taskVulnerability__level',
                'taskVulnerability__repair_method',
                'taskVulnerability__cve_num',
                'taskVulnerability__cnnvd_num',
                'taskVulnerability__dtime',
                'affectedServie',
                'taskAffectIP__ip'
            )
        else:
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
                'affectedServie',
                'taskAffectIP__ip'
            )
        toDtasksPage = Paginator(toDoTasks, 20)
        if request.method == "GET":
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                toDtasksPageObj = toDtasksPage.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                toDtasksPageObj = toDtasksPage.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                toDtasksPageObj = toDtasksPage.page(toDtasksPage.num_pages)

        return render(request, 'workBench/toDoMatters.html', {'toDtasksPage': toDtasksPageObj, })
    elif request.method == 'POST':
        doAction = request.POST.get('action')
        userScheduleControlerID = request.POST.get('tid')
        notetext = request.POST.get('notetext')
        print(notetext)
        targetUser = request.user.id
        targetUserObj = wxseUser.objects.get(id=targetUser)
        doResult = userScheduleControler.objects.get(id=userScheduleControlerID)
        doAction = int(doAction)
        if doAction == 0:
            doResult.status = 4
        elif doAction == 1:
            doResult.status = 3
        doResult.save()
        updateProgressNote = progressNote.objects.create(
            messageDetail=notetext,
            messageAuthor=targetUserObj.last_name + targetUserObj.last_name,
            userScheduleControlerNote=doResult,
        )
        updateProgressNote.save()
        return HttpResponse('success')


@login_required(login_url='/accounts/login')
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
        progressNoteObj = progressNote.objects.filter(userScheduleControlerNote=searchId).values(
            'messageDetail',
            'messageDate',
            'messageAuthor',
        )
        result = json.dumps({'queryResult': list(queryResult), 'queryIPResult': list(queryIPResult),
                             'queryProfessionsalWrokResult': list(queryProfessionsalWrokResult),
                             'progressNoteObj': list(progressNoteObj)}, cls=DjangoJSONEncoder)
        return HttpResponse(result)
    elif request.method == 'POST':
        doAction = request.POST.get('action')
        userScheduleControlerID = request.POST.get('tid')

        doResult = userScheduleControler.objects.get(id=userScheduleControlerID)
        if doAction == 0:
            doResult.status = 4
        elif doAction == 1:
            doResult.status = 3

        doResult.save()
        return None


@login_required(login_url='/accounts/login')
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
        result = json.dumps({'statusProgressValue': statusProgressValue, }, cls=DjangoJSONEncoder)
        return HttpResponse(result)
    else:
        finishTasks = userScheduleControler.objects.filter(taskUser=targetUser, status__gte=3).values(
            'id',
            'taskVulnerability__id',
            'taskVulnerability__name',
            'affectedServie',
            'taskVulnerability__detail',
            'taskVulnerability__level',
            'taskUser__first_name',
            'taskUser__last_name',
            'taskVulnerability__repair_method',
            'taskVulnerability__cve_num',
            'taskVulnerability__cnnvd_num',
            'taskVulnerability__dtime',
            'taskVulnerability__professionalwork__workName',
            'taskAffectIP__ip'
        )

    return render(request, 'workBench/finishMatters.html', {'finishTasks': finishTasks, })


@login_required(login_url='/accounts/login')
def closingMatters(request):
    targetUser = request.user.id
    closingTasks = userScheduleControler.objects.filter(taskUser=targetUser, status=7)
    closingTasksPage = Paginator(closingTasks, 20)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            closingTasksObj = closingTasksPage.page(page)
        except PageNotAnInteger:
            closingTasksObj = closingTasksPage.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            closingTasksObj = closingTasksPage.page(closingTasksPage.num_pages)
    return render(request, 'workBench/closingMatters.html', {'closingTasksPage': closingTasksObj})


def vulnerabilityDetailView(request):
    vulnerabilityDetailResult = vulnerability.objects.get()
    return None


def scheduleDetailView(request):
    return None


@login_required(login_url='/accounts/login')
def warningNotice(request):
    if request.method == 'GET':
        noticeNumQuery = request.GET.get('noticeNumQuery')
        noticeNameQuery = request.GET.get('noticeNameQuery')
        if noticeNumQuery or noticeNameQuery:
            warningNoticeResult = NoticeDetial.objects.filter(noticeName=noticeNameQuery)
        else:
            warningNoticeResult = NoticeDetial.objects.all()
        warningNoticeResultPage = Paginator(warningNoticeResult, 20)
        if request.method == "GET":
            page = request.GET.get('page')
            try:
                warningNoticeResultObj = warningNoticeResultPage.page(page)
            except PageNotAnInteger:
                warningNoticeResultObj = warningNoticeResultPage.page(1)
            except InvalidPage:
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                warningNoticeResultObj = warningNoticeResultPage.page(warningNoticeResultPage.num_pages)
        return render(request, 'workBench/warningNotice.html', {'warningNoticeResultPage': warningNoticeResultObj, })


    elif request.method == 'POST':
        noticeNum = request.POST.get('wid')
        returnData = NoticeDetial.objects.filter(id=noticeNum).values(
            'noticeName',
            'noticeDate',
            'noyiceStaff',
            'noticeLevel',
            'CVEserialNumber',
            'CNNVDserialNumber',
            'affectedVendor',
            'affectedComponent',
            'noticeDetail',
            'uploadfilesmanage__fileName',
            'uploadfilesmanage__fileUploadTo',
            'uploadfilesmanage__id',
        )
        result = json.dumps({'queryresult': list(returnData), }, cls=DjangoJSONEncoder)
        return HttpResponse(result)


@login_required(login_url='/accounts/login')
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


from configureDataBase.forms import UploadFileForm
import os
from configureDataBase.models.uploadFiles import uploadFilesManage


def handle_uploaded_file(fileName, files):
    writeCatalogue = os.path.join(os.path.abspath('.'), 'uploadFiles')
    fileFullPath = os.path.join(writeCatalogue, fileName)
    with open(fileFullPath, 'wb+') as destination:
        for chunk in files.chunks():
            destination.write(chunk)
    return fileFullPath


def uploadFile(request):
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        updateFileName = request.POST.get('fileName')

        fileFullPath = handle_uploaded_file(updateFileName, request.FILES['fileContent'])
        FilesID = uploadFilesManage.objects.create(
            fileName=updateFileName,
            fileUploadTo=fileFullPath)
        result = json.dumps({'FilesID': FilesID.id, }, cls=DjangoJSONEncoder)
        print(FilesID.id)
        return HttpResponse(result)
    else:
        return HttpResponse('ban')
    #     form = UploadFileForm()
    # return render(request, 'upload.html', {'form': form})


from django.http import StreamingHttpResponse,Http404
from django.utils.encoding import escape_uri_path

@login_required(login_url='/accounts/login')
def warningNoticeAppendixDownload(request):
    if request.method == 'GET':
        warningNoticeResult = NoticeDetial.objects.all()
        filesID = request.GET.get('filesID')
        # filepath = os.path.join(settings.MEDIA_ROOT, filename)
        fileObj = uploadFilesManage.objects.get(id=filesID)
        filepath = fileObj.fileUploadTo
        filename = fileObj.fileName
        try:
            print('attachment;filename="%s"' % filename)
            response = StreamingHttpResponse(open(filepath, 'rb'))
            # response = FileResponse(fp)
            response['Content-Type'] = 'application/octet-stream'
            # response['Content-Disposition'] = f'attachment;filename="%s"' % filename
            response['Content-Disposition'] = f'attachment;filename={escape_uri_path(filename)}'
            return response
        except Exception:
            raise Http404


@login_required(login_url='/accounts/login')
def warningNoticeAdd(request):
    if request.method == 'GET':
        warningNoticeResult = NoticeDetial.objects.all()
        return render(request, 'workBench/warningNoticeAdd.html', {'warningNoticeResult': warningNoticeResult, })
    elif request.method == 'POST':
        noticeNum = request.POST.get('noticeNum')
        noticeDate = request.POST.get('noticeDate')
        noticeName = request.POST.get('noticeName')
        noticeLevel = request.POST.get('noticeLevel')
        CVEserialNumber = request.POST.get('CVEserialNumber')
        CNNVDserialNumber = request.POST.get('CNNVDserialNumber')
        affectedVendor = request.POST.get('affectedVendor')
        noticeDetail = request.POST.get('noticeDetail')
        uploadNote = request.POST.get('uploadNote')
        print(noticeNum,
              noticeDate,
              noticeLevel,
              CVEserialNumber,
              affectedVendor, )
        targetNoticeDetial = NoticeDetial.objects.create(
            id=noticeNum,
            noticeDate=noticeDate,
            noticeName=noticeName,
            noticeLevel=noticeLevel,
            CVEserialNumber=CVEserialNumber,
            CNNVDserialNumber=CNNVDserialNumber,
            affectedVendor=affectedVendor,
            noticeDetail=noticeDetail,
        )
        if uploadNote:
            print(uploadNote)
            uploadFilesLink = uploadFilesManage.objects.get(id=uploadNote)
            uploadFilesLink.linkToNoticeDetial = NoticeDetial.objects.get(id=targetNoticeDetial.id)
            uploadFilesLink.save()

    return render(request, 'workBench/warningNoticeAdd.html', )


def navbarMenu(request):
    checkUser = request.user.id
    checkPrivilege = wxseUser.objects.get(id=checkUser).userPrivilege
    menuList = [
        ['发布事项', '/workbench/releasematters'],
        ['检查事项', '/workbench/checkmatters'],
        ['添加预警通告', '/workbench/warningnotice/add'],
    ]
    result = json.dumps(menuList, cls=DjangoJSONEncoder)
    if checkPrivilege == 0:
        return HttpResponse(result)
    else:
        return HttpResponse('ban')


def lastLogin(request):
    checkUser = request.user.id
    checkPrivilege = wxseUser.objects.get(id=checkUser).last_login
    result = json.dumps(checkPrivilege, cls=DjangoJSONEncoder)
    return HttpResponse(result)
