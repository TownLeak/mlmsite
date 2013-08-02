#!/usr/bin/python
# -*- coding: utf-8
from userena import views as userena_views
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.management import call_command
from models import User, MasterUser
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


def graph_eval(request):
    if request.method == 'POST':
        return ViewSupport.handleUserManagementForms_post(request, 'graph_eval.html')

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
        Controller().createNewBinaryPosition(user)
        Controller().createNewUnilevelPosition(user)
    return HttpResponseRedirect('/dev/graph_eval/')


def graph_eval_thousand_users(request):
    Controller().createManyNewUsers()
    return HttpResponseRedirect('/dev/graph_eval/')


def graph_eval_gyalu(request):
    call_command('flush', interactive=False, verbosity=1)
    call_command('syncdb', interactive=False, verbosity=1)
    return HttpResponseRedirect('//dev/graph_eval/')


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
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
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
