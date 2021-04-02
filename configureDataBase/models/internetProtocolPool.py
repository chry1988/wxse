from django.db import models


class IpV4(models.Model):
    vlan = models.IntegerField(default=0, blank=True)
    ip = models.GenericIPAddressField()
    area = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.ip)

    class Meta:
        verbose_name = 'IP地址'
        verbose_name_plural = 'IP地址'
