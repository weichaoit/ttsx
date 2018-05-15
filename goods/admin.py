from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id','gtitle','gpic','gprice','gclick','gkucun']
    list_per_page = 10


@admin.register(TypeInfo)
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']