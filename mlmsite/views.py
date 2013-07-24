#!/usr/bin/python
# -*- coding: utf-8
#from userena import views as userena_views
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.management import call_command
from models import User, MasterUser
from django.utils.translation import ugettext as _
from controller import Controller
from forms import GraphEval_UserSelectionForm, GraphEval_SponsorSelectionForm


def index(request):
    if request.method == 'POST':
        userSelectionForm = GraphEval_UserSelectionForm(request.POST, prefix="user")

        if userSelectionForm.is_valid():
            userSelectionForm.save()
            return HttpResponseRedirect('/')
    else:
        userSelectionForm = GraphEval_UserSelectionForm(prefix="user")

    #response = userena_views.signin(request, template_name='index.html')
    if Controller().getActualUser().isLoggedIn:
        return render(request, "index_loggedin.html", {
            "actual_user": Controller().getActualUser(),
            "userSelectionForm": userSelectionForm})
    else:
        return render(request, "index_notloggedin.html", {
            "actual_user": Controller().getActualUser(),
            "userSelectionForm": userSelectionForm})


def password_reset(request):
    return HttpResponse(_(u"Reset Password"))


def registration(request):
    return HttpResponse(_(u"Registration"))


def login(request):
    Controller().getActualUser().isLoggedIn = True
    return HttpResponseRedirect('/')


def logout(request):
    Controller().getActualUser().isLoggedIn = False
    return HttpResponseRedirect('/')


def bad_login(request):
    return HttpResponse(_(u"Hibás belépés"))


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

    return render(request, "graph_eval.html", {
        "actual_user": c.getActualUser(),
        "userSelectionForm": userSelectionForm,
        "sponsorSelectionForm": sponsorSelectionForm,
        "tree_data": c.getActualTree(),
        "actual_month": c.getActualMonth(),
        "tree_name": c.getActualTreeName(),
        "controller": c})


def graph_eval_more_users(request):
    for i in range(6):
        user = User.CreateNewUser(sponsor=MasterUser.Get())
        Controller().createNewBinaryPosition(user)
        Controller().createNewUnilevelPosition(user)
    return HttpResponseRedirect('/graph_eval/')


def graph_eval_thousand_users(request):
    Controller().createManyNewUsers()
    return HttpResponseRedirect('/graph_eval/')


def graph_eval_gyalu(request):
    call_command('flush', interactive=False, verbosity=1)
    call_command('syncdb', interactive=False, verbosity=1)
    return HttpResponseRedirect('/graph_eval/')


def graph_eval_leave(request, userid):
    c = Controller()
    c.userLeaves(User.objects.get(id=userid))
    return HttpResponseRedirect('/graph_eval/')


def graph_eval_binary_matrix(request):
    c = Controller()
    c.switchToBinaryMatrix()
    return HttpResponseRedirect('/graph_eval/')


def graph_eval_unilevel_matrix(request):
    c = Controller()
    c.switchToUnilevelMatrix()
    return HttpResponseRedirect('/graph_eval/')


def graph_eval_next_month(request):
    c = Controller()
    c.advanceToNextMonth()
    return HttpResponseRedirect('/graph_eval/')


def bootstrap(request):
    return render(request, "base_bootstrap_tutorial.html", {})

#from paypal.pro.views import PayPalPro
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
#from django.core.urlresolvers import reverse


def try_paypal_cancel(request):
    return render(request, "try_paypal_cancel.html", {})


def try_paypal_success(request):
    return render(request, "try_paypal_success.html", {})


from datetime import datetime


def try_paypal(request):
    paypal_dict = {"business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "1.00",             # amount to charge for item
        "invoice": datetime.now(),       # unique tracking variable paypal
        "item_name": "Cipő",
        "notify_url": "%s%s" % (settings.SITE_NAME, "atyalapatyala"),
        "cancel_return": "%s/try_paypal_cancel" % settings.SITE_NAME,  # Express checkout cancel url
        "return_url": "%s/try_paypal_success" % settings.SITE_NAME}  # Express checkout return url

    # kw = {"item": item,                            # what you're selling
    #     "payment_template": "try_paypal.html",      # template name for payment
    #     "confirm_template": "try_paypal_confirmation.html",  # template name for confirmation
    #     "success_url": "/try_paypal_success/"}              # redirect location after success

    #ppp = PayPalPro(**kw)
    #return ppp(request)
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form.sandbox()}
    return render(request, "try_paypal.html", context)
