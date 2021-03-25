from django.db import models
from .vulnerabilityControler import vulnerability
from ..configureChoices import userScheduleControlerChoices, adminScheduleControlerChoices


class userScheduleControler(models.Model):
    # user = models.ForeignKey()
    status = models.CharField(choices=userScheduleControlerChoices, max_length=50)
    taskVulnerability = models.ForeignKey(vulnerability, on_delete=models.DO_NOTHING)


class adminScheduleControler(models.Model):
    # user = models.ForeignKey()
    status = models.CharField(choices=adminScheduleControlerChoices, max_length=50)
    taskVulnerability = models.ForeignKey(vulnerability, on_delete=models.DO_NOTHING)
