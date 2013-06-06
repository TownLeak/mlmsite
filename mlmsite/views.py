#!/usr/bin/python
# -*- coding: utf-8
from userena import views as userena_views
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.management import call_command


def index(request):
    response = userena_views.signin(request, template_name='index.html')
    return response


from forms import GraphEval_UserSelectionForm, GraphEval_SponsorSelectionForm
from controller import Controller


def graph_eval(request):
    if request.method == 'POST':
        userSelectionForm = GraphEval_UserSelectionForm(request.POST, prefix="user")
        sponsorSelectionForm = GraphEval_SponsorSelectionForm(request.POST, prefix="sponsor")

        if userSelectionForm.is_valid():
            userSelectionForm.save()
            return HttpResponseRedirect('/graph_eval/')

        if sponsorSelectionForm.is_valid():
            sponsorSelectionForm.save()
            return HttpResponseRedirect('/graph_eval/')
    else:
        userSelectionForm = GraphEval_UserSelectionForm(prefix="user")
        sponsorSelectionForm = GraphEval_SponsorSelectionForm(prefix="sponsor")

    c = Controller()
    nodes = c.getActualData()

    return render(request, "graph_eval.html", {
        "actual_user": c.getActualUser(),
        "userSelectionForm": userSelectionForm,
        "sponsorSelectionForm": sponsorSelectionForm,
        "nodes": nodes})


def graph_eval_more_users(request):
    c = Controller()
    master = c.getMaster()
    for i in range(6):
        user = c.createNewUser(sponsor=master)
        c.createNewPosition(user)
    return HttpResponseRedirect('/graph_eval/')


def graph_eval_gyalu(request):
    call_command('flush', interactive=False, verbosity=1)
    call_command('syncdb', interactive=False, verbosity=1)
    return HttpResponseRedirect('/graph_eval/')


def bootstrap(request):
    return render(request, "base_bootstrap_tutorial.html", {})
