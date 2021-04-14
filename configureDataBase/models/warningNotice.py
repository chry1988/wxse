from django.db import models


class NoticeDetial(models.Model):
    '''
    通告编号
    附件
    '''
    noticeName = models.CharField(max_length=255, verbose_name='通告名称')
    noticeDate = models.DateTimeField(verbose_name='通告时间')
    noyiceStaff = models.CharField(max_length=255, verbose_name='通告人员')
    noticeLevel = models.CharField(max_length=255, verbose_name='严重级别')
    CVEserialNumber = models.CharField(max_length=255, verbose_name='CVE编号')
    CNNVDserialNumber = models.CharField(max_length=255, verbose_name='CNNVD编号')
    affectedVendor = models.CharField(max_length=255, verbose_name='影响厂商')
    affectedComponent = models.CharField(max_length=255, verbose_name='影响组件')
    noticeDetail = models.TextField(verbose_name='通告描述')
