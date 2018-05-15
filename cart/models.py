from django.db import models

# Create your models here.

class CartInfo(models.Model):
    user = models.ForeignKey('user.UserInfo',on_delete=models.DO_NOTHING)
    goods = models.ForeignKey('goods.GoodsInfo',on_delete=models.DO_NOTHING)
    count = models.IntegerField()

