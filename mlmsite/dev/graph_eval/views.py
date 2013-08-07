#!/usr/bin/python
# -*- coding: utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.management import call_command
from mlmsite.models import User, MasterUser
from mlmsite.controller import Controller
from django.conf import settings

if settings.DEVELOPMENT_MODE:
    from mlmsite.dev.view_support import ViewSupport
else:
    from mlmsite.view_support import ViewSupport


def graph_eval(request):
    if request.method == 'POST':
        return ViewSupport.handleUserManagementForms_post(request, '')

    c = Controller()

    context = {
        "actual_user": c.getActualUser(),
        "tree_data": c.getActualTree(),
        "actual_month": c.getActualMonth(),
        "tree_name": c.getActualTreeName(),
        "controller": c}

    context.update(ViewSupport.handleUserManagementForms_get(request))
    return render(request, "graph_eval.html", context)


def graph_eval_more_users(request):
    for i in range(6):
        user = User.CreateNewUser(sponsor=MasterUser.Get())
        Controller().createNewBinaryPosition(user.id)
        Controller().createNewUnilevelPosition(user.id)
    return HttpResponseRedirect('/dev/graph_eval/')


def graph_eval_thousand_users(request):
    Controller().createManyNewUsers()
    return HttpResponseRedirect('/dev/graph_eval/')


def graph_eval_gyalu(request):
    call_command('flush', interactive=False, verbosity=1)
    call_command('syncdb', interactive=False, verbosity=1)
    return HttpResponseRedirect('/dev/graph_eval/')


def graph_eval_leave(request, userid):
    c = Controller()
    c.userLeaves(User.objects.get(id=userid))
    return HttpResponseRedirect('/dev/graph_eval/')


def graph_eval_binary_matrix(request):
    c = Controller()
    c.switchToBinaryMatrix()
    return HttpResponseRedirect('/dev/graph_eval/')


def graph_eval_unilevel_matrix(request):
    c = Controller()
    c.switchToUnilevelMatrix()
    return HttpResponseRedirect('/dev/graph_eval/')


def graph_eval_next_month(request):
    c = Controller()
    c.advanceToNextMonth()
    return HttpResponseRedirect('/dev/graph_eval/')
