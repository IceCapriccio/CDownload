"""CSDN URL Configuration

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
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.views import static

# my views
from . import view, db_demo
urlpatterns = [
    url(r'^admin123/', admin.site.urls),

    url(r'^db$', db_demo.testdb),
    url(r'^register$', view.register),
    url(r'^solve_register$', view.solve_register),
    url(r'^login', view.login),
    url(r'^solve_login', view.solve_login),
    url(r'^download$', view.download),
    url(r'^solve_download', view.solve_download),
    url(r'^solve_logout', view.solve_logout),
    url(r'^update$', db_demo.update),
    url(r'^solve_update', db_demo.solve_update),
    url(r'^recharge$', view.recharge),
    url(r'^solve_recharge$', view.solve_recharge),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]

