#!/usr/bin/python
# -*- coding: utf-8
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import PostalAddressForm, SignupForm
from userena.views import signup as userena_signup


def signup(request):
    if request.method == 'POST':
        postal_form = PostalAddressForm(request.POST, prefix=_(u"Postal"))
        delivery_form = PostalAddressForm(request.POST, prefix=_(u"Delivery"))
    else:
        postal_form = PostalAddressForm(prefix=_(u"Postal"))
        delivery_form = PostalAddressForm(prefix=_(u"Delivery"))

    def signup_form(*args, **kw):
        return SignupForm(postal_form, delivery_form, *args, **kw)

    return userena_signup(request,
        signup_form=signup_form,
        template_name='signup.html',
        extra_context = {
            'postal_form': postal_form,
            'delivery_form': delivery_form}
    )


# -----------------------------------------------------------------------------
def postaladdress(request):
    if request.method == 'POST':
        postal_form = PostalAddressForm(request.POST, prefix=_(u"Postal"))
        delivery_form = PostalAddressForm(request.POST, prefix=_(u"Delivery"))
        if postal_form.is_valid() and delivery_form.is_valid():
            return HttpResponseRedirect('/')
    else:
        postal_form = PostalAddressForm(prefix=_(u"Postal"))
        delivery_form = PostalAddressForm(prefix=_(u"Delivery"))

    return render(request, "signup.html", {
        'postal_form': postal_form,
        'delivery_form': delivery_form}
    )
