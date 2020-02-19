# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from rest_framework import routers
from api import views
from rest_framework import routers, serializers, viewsets


urlpatterns = [
      # add your own patterns here
      url('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
      url('start/', views.update_prices),
      url('crypto/(?P<symbol>\w{0,50})/', views.get_crypto,name='getcrypto'),
      url('global/', views.get_global, name='getglobal'),
      url('asset/(?P<symbol>\w{0,50})/', views.get_asset, name="getasset"),
      url('hist/(?P<symbol>\w{0,50})/', views.get_recent_history),
      url('symbols/', views.get_symbols, name='symbols'),
      url('marketcaps/', views.get_marketcap, name='marketcaps'),
      url('ratios/', views.get_ratio_staked_circ, name='ratios')
  ]
