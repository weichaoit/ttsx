from django.db import models

# Create your models here.
class OrderInfo(models.Model):
    oid = models.CharField('订单id',max_length=32,primary_key=True)
    user = models.ForeignKey('user.UserInfo',models.DO_NOTHING)
    odata = models.DateTimeField('创建时间',auto_now_add=True)
    oIsPay = models.BooleanField('是否支付',default=False)
    ototal = models.DecimalField('总计',max_digits=10,decimal_places=2)
    oaddress = models.CharField('地址信息',max_length=200)


class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('goods.GoodsInfo',on_delete=models.DO_NOTHING)
    order = models.ForeignKey('OrderInfo',on_delete=models.DO_NOTHING)
    price = models.DecimalField('商品价格小计',max_digits=9,decimal_places=2)
    count = models.IntegerField()