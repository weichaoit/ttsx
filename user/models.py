from django.db import models

# Create your models here.

class UserInfo(models.Model):
    uname = models.CharField(max_length=32)
    upwd = models.CharField(max_length=64)
    uemail = models.CharField(max_length=32)
    ushou = models.CharField(max_length=32,default='')
    uaddress = models.CharField(max_length=128,default='')
    uyoubian = models.CharField(max_length=8,default='')
    uphone = models.CharField(max_length=11,default='')
