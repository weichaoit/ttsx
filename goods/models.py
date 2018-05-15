from django.db import models
from DjangoUeditor.models import UEditorField


# Create your models here.
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=32)
    isDelete = models.BooleanField(max_length=False)

    def __str__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=32,verbose_name='商品名称')
    gpic = models.ImageField(upload_to='goods',verbose_name='商品图片')
    gprice = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='价格')
    gunit = models.CharField(max_length=32,default='500g',verbose_name='质量')
    gclick = models.IntegerField(verbose_name='点击量')
    gjianjie = models.CharField(max_length=256,verbose_name='简介')
    gkucun = models.IntegerField(verbose_name='库存')
    gcontent = UEditorField(verbose_name='详细信息',width='600',height='300',toolbars='full',imagePath='static/ueditor/')
    idDelete = models.BooleanField(default=False)
    gtype = models.ForeignKey('TypeInfo',on_delete=models.DO_NOTHING,verbose_name='商品分类')
    gadv = models.BooleanField(default=False,verbose_name='广告位')