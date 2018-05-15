from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^register_handle/$',views.register_handle),
    url(r'^registe_exist/$',views.registe_exist),
    url(r'^login/$',views.login),
    url(r'^info/$',views.info),
    url(r'^log_out/$',views.log_out),
    url(r'^order/$',views.order),
    url(r'^site/$',views.site),
    url(r'^redirect_msg/$',views.redirect_msg)
]