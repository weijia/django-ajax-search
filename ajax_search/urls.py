from django.conf.urls import *
from ajax_search import views

urlpatterns = patterns('',
                       url(r'^xhr_search$', views.xhr_search),
                       url(r'^search/', views.search),
                       )
