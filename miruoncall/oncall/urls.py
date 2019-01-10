# -*- coding: utf-8 -*-

from django.urls import path

from oncall.views import Oncall

urlpatterns = [
    path('<team_id>', Oncall.as_view()),
]
