#!/usr/bin/python
# -*- coding: utf-8
from userena import views as userena_views
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from controller import Controller
from django.conf import settings

if settings.DEVELOPMENT_MODE:
    from mlmsite.dev.view_support import ViewSupport
else:
    from mlmsite.view_support import ViewSupport


def index(request):
    if request.method == 'POST':
        if "submit_login" in request.POST:
            return userena_views.signin(request)
        else:
            return ViewSupport.handleUserManagementForms_post(request, "/")

    template = "index_loggedin.html" if Controller().getActualUser().isLoggedIn else "index_notloggedin.html"
    extra_context = ViewSupport.handleUserManagementForms_get(request)
    return userena_views.signin(request, template_name=template, extra_context=extra_context)


def password_reset(request):
    return render(request, "password_reset.html", {})


def registration(request):
    if request.method == 'POST':
        return ViewSupport.handleUserManagementForms_post(request, '/')
    return render(request, "registration.html", ViewSupport.handleUserManagementForms_get(request))


def login(request):
    Controller().getActualUser().isLoggedIn = True
    return HttpResponseRedirect('/')


def logout(request):
    Controller().getActualUser().isLoggedIn = False
    return HttpResponseRedirect('/')


def bad_login(request):
    return HttpResponse(_(u"Bad login"))
