from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$',views.cart),
    url(r'^add/$',views.add),
    url(r'^delete/$',views.delete),
    url(r'^edit/$',views.edit)
]