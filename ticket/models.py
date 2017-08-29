# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Ticket(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=20)
    time = models.CharField(verbose_name="开车时间", max_length=40)
    dist = models.CharField(verbose_name="乘车区间", max_length=40)
    no = models.CharField(verbose_name="车次", max_length=10)
    seat = models.CharField(verbose_name="座位", max_length=20)
    sender = models.CharField(verbose_name="发信邮箱", max_length=50)

    def __unicode__(self):
        return "{}/{}/{}".format(self.name,self.dist,self.time)