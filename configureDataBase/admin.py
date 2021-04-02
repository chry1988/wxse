from django.contrib import admin
from .models.workBench import userScheduleControler, adminScheduleControler
from .models.vulnerabilityControler import vulnerability


class userScheduleControlerAdmin(admin.ModelAdmin):
    pass


admin.site.register(userScheduleControler, userScheduleControlerAdmin)


class adminScheduleControlerAdmin(admin.ModelAdmin):
    pass


admin.site.register(adminScheduleControler, adminScheduleControlerAdmin)


class vulnerabilityAdmin(admin.ModelAdmin):
    pass


admin.site.register(vulnerability, vulnerabilityAdmin)
