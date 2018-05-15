from django.contrib import admin
from .models import UserInfo
# Register your models here.

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id','uname']


# admin.site.register(UserInfo)