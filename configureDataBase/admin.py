from django.contrib import admin
from .models.workBench import userScheduleControler, adminScheduleControler, progressNote
from .models.vulnerabilityControler import vulnerability, professionalWork
from .models.warningNotice import NoticeDetial
from .models.internetProtocolPool import IpV4
from .models.uploadFiles import *


class userScheduleControlerAdmin(admin.ModelAdmin):
    pass


admin.site.register(userScheduleControler, userScheduleControlerAdmin)


class adminScheduleControlerAdmin(admin.ModelAdmin):
    pass


admin.site.register(adminScheduleControler, adminScheduleControlerAdmin)


class vulnerabilityAdmin(admin.ModelAdmin):
    pass


admin.site.register(vulnerability, vulnerabilityAdmin)


class professionalWorkAdmin(admin.ModelAdmin):
    pass


admin.site.register(professionalWork, professionalWorkAdmin)


class NoticeDetialAdmin(admin.ModelAdmin):
    pass


admin.site.register(NoticeDetial, NoticeDetialAdmin)


class IpV4Admin(admin.ModelAdmin):
    pass


admin.site.register(IpV4, IpV4Admin)


class progressNoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(progressNote, progressNoteAdmin)


class uploadFilesManageAdmin(admin.ModelAdmin):
    pass


admin.site.register(uploadFilesManage, uploadFilesManageAdmin)
