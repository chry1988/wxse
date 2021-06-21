from django.db import models
from ..models.warningNotice import NoticeDetial
import os


def defaultuUploadPath():
    return os.path.join(os.path.abspath('.'), 'uploadFiles')


class uploadFilesManage(models.Model):
    fileName = models.CharField(max_length=255, verbose_name='上传文件')
    fileUploadTo = models.FilePathField(path=defaultuUploadPath)
    linkToNoticeDetial = models.ForeignKey(NoticeDetial, on_delete=models.CASCADE)
