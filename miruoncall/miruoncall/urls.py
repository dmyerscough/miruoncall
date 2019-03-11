"""miruoncall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include, path
from rest_framework.authtoken import views

from account import urls as account_urls
from dashboard import urls as dashboard_urls
from miruoncall.views import healthz
from oncall import urls as oncall_urls

urlpatterns = [
    path('', include(oncall_urls)),
    path('accounts/', include(account_urls)),
    path('auth/', views.obtain_auth_token),
    path('dashboard/', include(dashboard_urls)),
    path('healthz/', healthz, name='healthz'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls)),
    )
