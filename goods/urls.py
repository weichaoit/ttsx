from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    url(r'^$',views.index),
    url(r'^list_(\d+)_(\d+)_(\d+)/$',views.lists),
    url(r'^detail_(\d+)/$',views.detail),
    url(r'^search/',MySearchView())
]