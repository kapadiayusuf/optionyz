from django.conf.urls import include
from django.urls import path

from django.urls import re_path
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.showDashboard, name='Index'),
    re_path(r'^heatmap/$', views.showHeatmap,name='trends'),
    re_path(r'^heatmap/(?P<sort>.*)/$', views.showHeatmap,name='trends'),
    re_path(r'^screeners/$', views.showScreener,name='trends'),
    re_path(r'^screeners/(?P<scrip>.*)/$', views.showScreener,name='trends'),
    re_path(r'^top20/$', views.showTop20,name='trends'),
    re_path(r'^tv_top20/$', views.showTvTop20,name='trends'),
    re_path(r'^df/$', views.showDataframe,name='trends'),
    re_path(r'^gen20DFuturesBU.*$', views.gen20DFuturesBU , name = 'gen20DFuturesBU'),
    re_path(r'^completeFuturesAnalysis.*$', views.completeFuturesAnalysis , name = 'completeFuturesAnalysis'),
    re_path(r'^gen20DOptionsOI.*$', views.gen20DOptionsOI , name = 'gen20DOptionsOI'),
    path('refresh_json/' , views.refresh_json, name = 'refresh_json'),
    path('futuresOptionsMR/', views.getFuturesOptionsMR, name = 'FuturesOptionsMR'),
    path('20DFuturesBU/', views.load20DFuturesBU, name = '20DFuturesBU'),
    path('webhook/VSLRT/', views.webhook_VSLRT, name='webhook_VSLRT'),
    path('webhook/lorentz/', views.webhook_lorentz, name='webhook_lorentz'),
    path('webhook/lorentz_multiTF/', views.webhook_lorentz_multiTimeframe, name='webhook_lorentz_multiTimeframe')
    #path('gen20DFuturesBU/', views.gen20DFuturesBU , name = 'gen20DFuturesBU')
    
    # url(r'^trends/$', views.showTrends,name='trends'),


    # url(r'^charts/(?P<symbol>.*)/$', views.showCharts,name='charts'),
    # url(r'^charts/$', views.showCharts,name='charts'),
]