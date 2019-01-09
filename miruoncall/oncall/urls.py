# -*- coding: utf-8 -*-

from django.urls import path

from oncall.views import Oncall

urlpatterns = [
    path('', Oncall.as_view()),
]
