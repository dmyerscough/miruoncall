# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from oncall.models import Team


@login_required
def index(request):
    """
    Render Dashboard
    """
    team = Team.objects.all().order_by('name')[0]

    return render(request, 'dashboard/index.html', {'team': team})
