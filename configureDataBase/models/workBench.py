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


class adminScheduleControler(models.Model):
    status = models.IntegerField(choices=adminScheduleControlerChoices, )
    taskVulnerability = models.ForeignKey(vulnerability, on_delete=models.DO_NOTHING)
    taskUser = models.ForeignKey(wxseUser, on_delete=models.CASCADE)
    deadLine = models.DateTimeField(default=datetime.now, blank=True)
