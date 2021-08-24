from django.shortcuts import render
from .models import wxseUser
from .models import wxseDepartment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import render, HttpResponse


# Create your views here.
def listCustomUser(request):
    '''


    :param request:
    :return:
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff
    userGroup = models.CharField(verbose_name='组别', max_length=3, default=4)
    userPrivilege = models.IntegerField(verbose_name='权限', default=0)
    userPhone = models.CharField(verbose_name='联系电话', max_length=30, blank=True, null=True)
    '''

    customUserQuery = wxseUser.objects.only('username', 'first_name', 'last_name', 'is_active', 'userPhone', 'is_staff',
                                            'is_superuser')
    # groups = wxseDepartment.objects.only('name').all()
    query_dict = {}
    # # 检索
    # groups__id = request.GET.get('group')
    # if groups__id:
    #     try:
    #         group_id = int(groups__id)
    #         query_dict['groups__id'] = groups__id
    #     except Exception as e:
    #         pass

    is_staff = request.GET.get('is_staff')
    if is_staff == '0':
        query_dict['is_staff'] = False
    if is_staff == '1':
        query_dict['is_staff'] = True

    is_superuser = request.GET.get('is_superuser')
    if is_superuser == '0':
        query_dict['is_superuser'] = False
    if is_superuser == '1':
        query_dict['is_superuser'] = True

    username = request.GET.get('username')

    if username:
        query_dict['username'] = username

    customUserPage = Paginator(customUserQuery, 20)
    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            customUserPageObj = customUserPage.page(page)
        except PageNotAnInteger:
            customUserPageObj = customUserPage.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            customUserPageObj = customUserPage.page(customUserPage.num_pages)
    return render(request, 'customUser/userManage.html',
                  {'customUserPage': customUserPageObj, 'customUserQuery':customUserQuery})
