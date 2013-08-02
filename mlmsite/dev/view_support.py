#!/usr/bin/python
# -*- coding: utf-8
from forms import GraphEval_UserSelectionForm, GraphEval_SponsorSelectionForm
from django.http import HttpResponseRedirect
from mlmsite.controller import Controller
from mlmsite.view_support import ViewSupportBase


class ViewSupport(ViewSupportBase):
    @classmethod
    def handleUserManagementForms_get(cls, request):
        return {"actual_user": Controller().getActualUser(),
                "userSelectionForm": GraphEval_UserSelectionForm(prefix="user"),
                "sponsorSelectionForm": GraphEval_SponsorSelectionForm(prefix="sponsor")}

    @classmethod
    def handleUserManagementForms_post(cls, request, redirect_url):
        """Handles the user selection and user creation forms. The forms simulate successful user registration
           and an user session: the system will behave in behalf of teh selected user.

           In case of POST, the function handles/validates the form, then redirects to redirect_url.
           Otherwise, it returns the data of the forms, prefixed by "user" and "sponsor"."""
        userSelectionForm = GraphEval_UserSelectionForm(request.POST, prefix="user")
        sponsorSelectionForm = GraphEval_SponsorSelectionForm(request.POST, prefix="sponsor")

        if userSelectionForm.is_valid():
            userSelectionForm.save()
            return HttpResponseRedirect(redirect_url)

        if sponsorSelectionForm.is_valid():
            sponsorSelectionForm.save()
            return HttpResponseRedirect(redirect_url)

        return None

