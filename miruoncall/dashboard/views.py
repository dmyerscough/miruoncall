# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    """
    Render Dashboard
    """
    return render(request, 'dashboard/index.html')
