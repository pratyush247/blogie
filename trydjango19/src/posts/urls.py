from django.conf.urls import url
from django.contrib import admin

from .views import (
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	)
#above method is for 1.10 for error arguments deprecated call the callable
#old method from . import views
	##url(r'^create/$', "view.<function_name"),
#from posts import views
#from post2 import views
#since two same views so #from posts import views as post2_view required so better to use method 2 as down
urlpatterns = [
    #method 1 importing views
  	#  url(r'^posts/$', "views.post_home"),
  	#method 2 without importing views
    url(r'^$',post_list,name="list"), #default home when typed posts in navigation
    url(r'^create/$', post_create),
    url(r'^(?P<slug>[\w-]+)/$',post_detail,name="detail"),
    url(r'^(?P<slug>[\w-]+)/update/$',post_update),
    url(r'^(?P<slug>[\w-]+)/delete/$',post_delete),

    #url(r'^posts/$', "<appname>.view.<function_name"),

]
 #url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
  #  url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
   # url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),