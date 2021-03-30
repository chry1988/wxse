from django.db import models
from .vulnerabilityControler import vulnerability
from ..configureChoices import userScheduleControlerChoices, adminScheduleControlerChoices
from customUser.models import wxseUser

class userScheduleControler(models.Model):
    status = models.CharField(choices=userScheduleControlerChoices, max_length=50)
    taskVulnerability = models.ForeignKey(vulnerability, on_delete=models.DO_NOTHING)
    taskUser = models.ForeignKey(wxseUser, on_delete=models.CASCADE)


class adminScheduleControler(models.Model):
    status = models.CharField(choices=adminScheduleControlerChoices, max_length=50)
    taskVulnerability = models.ForeignKey(vulnerability, on_delete=models.DO_NOTHING)
    taskUser = models.ForeignKey(wxseUser, on_delete=models.CASCADE)
