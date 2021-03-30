from django.db import models
from django.contrib.auth.models import AbstractUser


class wxseUser(AbstractUser):
    userDepartment = models.CharField(verbose_name='部门', max_length=3, default=0)
    userGroup = models.CharField(verbose_name='组别', max_length=3, default=4)
    userPrivilege = models.IntegerField(verbose_name='网络权限', default=0)
    userPhone = models.CharField(verbose_name='联系电话', max_length=30, blank=True, null=True)
