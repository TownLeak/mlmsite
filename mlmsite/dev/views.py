#!/usr/bin/python
# -*- coding: utf-8
from django.shortcuts import render
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm


def bootstrap(request):
    return render(request, "base_bootstrap_tutorial.html", {})


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
