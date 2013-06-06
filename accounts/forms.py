from django import forms
from django.forms import extras
from django.utils.translation import ugettext_lazy as _
from userena import forms as userena_forms
from django_countries.countries import COUNTRIES

from utils import DateTimeFactory, MinAgeFactory
from models import PostalAddress


class PostalAddressForm(forms.Form):
    address = forms.CharField(
        label=_(u'Address'),
        required=True
    )

    city = forms.CharField(
        label=_(u"City"),
        required=True
    )

    state = forms.CharField(
        label=_(u"State or province"),
        required=False
    )

    zip_code = forms.CharField(
        label=_(u"Zip code"),
        required=True)

    country = forms.ChoiceField(
        COUNTRIES,
        label=_(u"Country"),
        required=True, initial='HU'
    )


# ------------------------------------------------------------------------------
class SignupForm(userena_forms.SignupForm):
    """
    Class: SignupForm
    The form to sign up a new user.

    Attribute: first_name
    First name of the user.

    Attribute: last_name
    Last name of the user.

    Attribute: birth_date
    Birth date of the user.
    """

    __birthdate_widget = extras.SelectDateWidget(
        years=range(DateTimeFactory.getToday().year - MinAgeFactory.getMinAge(), 1899, -1))

    first_name = forms.CharField(label=_(u'First name'), required=True)

    last_name = forms.CharField(label=_(u'Last name'), required=True)

    birth_date = forms.DateField(label=_(u'Birth date'), required=True, widget=__birthdate_widget)

    def __init__(self, p_address, d_address, *args, **kw):
        self.postal_form = p_address
        self.delivery_form = d_address
        super(SignupForm, self).__init__(*args, **kw)

    def is_valid(self):
        return self.postal_form.is_valid() and\
            self.delivery_form.is_valid() and\
            super(SignupForm, self).is_valid()

    def __fillAddress(self, model, form):
        model.address = form.cleaned_data['address']
        model.city = form.cleaned_data['city']
        model.state = form.cleaned_data['state']
        model.zip_code = form.cleaned_data['zip_code']
        model.country = form.cleaned_data['country']
        model.save()

    def save(self):
        """
        Override the save method to save the first and last name to the user
        field.
        """
        # First save the parent form and get the user.
        new_user = super(SignupForm, self).save()
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        profile = new_user.get_profile()
        profile.birth_date = self.cleaned_data['birth_date']
        profile.postal_address = PostalAddress.objects.create()
        self.__fillAddress(profile.postal_address, self.postal_form)
        profile.delivery_address = PostalAddress.objects.create()
        self.__fillAddress(profile.delivery_address, self.delivery_form)
        profile.save()

        # Userena expects to get the new user from this form, so return the new user.
        return new_user
