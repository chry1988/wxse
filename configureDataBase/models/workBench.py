from django.db import models
from datetime import datetime
from .vulnerabilityControler import vulnerability
from ..configureChoices import userScheduleControlerChoices, adminScheduleControlerChoices
from .internetProtocolPool import IpV4
from customUser.models import wxseUser


class userScheduleControler(models.Model):
    status = models.IntegerField(choices=userScheduleControlerChoices, )
    taskVulnerability = models.ForeignKey(vulnerability, on_delete=models.DO_NOTHING)
    taskUser = models.ForeignKey(wxseUser, on_delete=models.CASCADE)
    deadLine = models.DateTimeField(default=None, blank=True)
    taskAffectIP = models.ManyToManyField(IpV4, default=None, blank=True)
    affectedServie = models.CharField(max_length=255, verbose_name='影响业务')


class adminScheduleControler(models.Model):
    status = models.IntegerField(choices=adminScheduleControlerChoices, )
    taskVulnerability = models.ForeignKey(vulnerability, on_delete=models.DO_NOTHING)
    taskUser = models.ForeignKey(wxseUser, on_delete=models.CASCADE)
    deadLine = models.DateTimeField(default=datetime.now, blank=True)


class progressNote(models.Model):
    messageDetail = models.TextField()
    messageDate = models.DateTimeField(auto_now=True)
    messageAuthor = models.CharField(max_length=255)
    userScheduleControlerNote = models.ForeignKey(userScheduleControler, on_delete=models.CASCADE)
