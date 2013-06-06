from django.utils import unittest
from django.utils.translation import ugettext_lazy as _
from userena.tests.profiles.test import ProfileTestCase
from userena.models import UserenaSignup
from forms import SignupForm
from django.contrib.auth.models import User
from forms import PostalAddressForm


class TestSignupForm(ProfileTestCase):
    msg_field_required = _(u'This field is required.')

    f_valid_form_data = {
        'username': "Zsolt",
        'first_name': "a@c.com",
        'last_name': "testuser",
        'email': "a@c.com",
        'password1': "password",
        'password2': "password",
        'birth_date': "1974-05-23"
    }

    f_valid_postal_address_form_data = {
        'address': "address1",
        'city': "City",
        'state': "State",
        'zip_code': "12345",
        'country': 'HU'
    }

    f_postal_address_form = PostalAddressForm(f_valid_postal_address_form_data)

    def setUp(self):
        # Setup userena permissions
        UserenaSignup.objects.check_permissions()

    def testRequiredFields(self):
        for f in ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'birth_date']:
            form_data = self.f_valid_form_data.copy()
            form_data[f] = ''
            form = SignupForm(self.f_postal_address_form, self.f_postal_address_form, data=form_data)
            self.assertEqual(form.is_valid(), False, "Form must not be valid with empty field %s" % f)

    def testPersistency(self):
        """
        Test if an user had been saved to the database, and its properties are saved well
        (i.e. the field values correspond to those of the fixture)
        """
        form_data = self.f_valid_form_data.copy()
        form = SignupForm(self.f_postal_address_form, self.f_postal_address_form, data=form_data)
        self.assertEqual(form.is_valid(), True)
        form.save()
        user = User.objects.get(username=form_data['username'])
        self.assertEqual(user.username, form_data['username'])
        profile = user.get_profile()

        # Check presence of postal addresses
        self.assertEqual(profile.postal_address.city, self.f_valid_postal_address_form_data['city'])
        self.assertEqual(profile.delivery_address.city, self.f_valid_postal_address_form_data['city'])
        user.delete()

    def testValidForm(self):
        form = SignupForm(self.f_postal_address_form, self.f_postal_address_form, data=self.f_valid_form_data)
        self.assertEqual(form.is_valid(), True)
        "Here, it must not raise..."
        form.save()
        user = User.objects.get(username=self.f_valid_form_data['username'])
        user.delete()


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(TestSignupForm)
