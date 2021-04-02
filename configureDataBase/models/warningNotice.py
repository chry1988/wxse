from django.db import models


class NoticeDetial(models.Model):
    '''通告编号
    影响厂商
    '''
    noticeName = models.CharField(verbose_name='通告名称')
    noticeDate = models.DateTimeField(verbose_name='通告时间')
    noticeLevel = models.CharField(verbose_name='严重级别')
    CVEserialNumber = models.CharField(verbose_name='CVE编号')
    CNNVDserialNumber = models.CharField(verbose_name='CNNVD编号')
