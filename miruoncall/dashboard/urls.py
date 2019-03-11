# -*- coding: utf-8 -*-

from django.urls import path

from dashboard.views import index

urlpatterns = [
    path('', index, name='dashboard_index'),
]
