import datetime

from dateutil import parser
from django.utils import unittest
from django.test import TestCase
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from accounts.models import UserProfile, PostalAddress


class TestUserProfile(TestCase):
    f_postal_address = {
        'address': "address1",
        'city': "City",
        'state': "State",
        'zip_code': "12345",
        'country': 'HU'
    }

    f_username = "testusername1"

    f_birth_date = "1974-05-23"

    f_fixture = {
        'birth_date': f_birth_date,
        'postal_address': PostalAddress(**f_postal_address.copy()),
        'delivery_address': PostalAddress(**f_postal_address.copy()),
        'user': User(username=f_username),
    }

    def __copyFixture(self):
        """
        Deep copy of the fixture objects
        """
        f = self.f_fixture.copy()
        f['postal_address'] = PostalAddress(**self.f_postal_address.copy())
        f['delivery_address'] = PostalAddress(**self.f_postal_address.copy())
        return f

    # -------------------------------------------------------------------------
    def testBlankBirthDate(self):
        """
        Must raise ValidationError.
        """
        f = self.__copyFixture()
        f['birth_date'] = ''
        with self.assertRaises(ValidationError):
            UserProfile(**f)

    # -------------------------------------------------------------------------
    def testValidBirthDate(self):
        # Must not raise exception
        up = UserProfile(**self.f_fixture)
        dt = parser.parse(self.f_birth_date)
        self.assertEqual(dt.date(), up.birth_date)

    # -------------------------------------------------------------------------
    def testTooYoungClient(self):
        f = self.__copyFixture()
        f['birth_date'] = "%d-01-01" % datetime.date.today().year
        # Must raise exception
        with self.assertRaises(ValidationError) as cm:
            up = UserProfile(**f)
            up.full_clean()

        err = cm.exception
        self.assertIn(_(u"You must be min"), err.messages[0])

    # -------------------------------------------------------------------------
    def testValidPostalAddresses(self):
        # Must not raise exception
        up = UserProfile(**self.f_fixture)
        self.assertEqual(self.f_postal_address['address'], up.postal_address.address)
        self.assertEqual(self.f_postal_address['address'], up.delivery_address.address)

    # -------------------------------------------------------------------------
    def testInvalidPostalAddresses(self):
        for field in ['postal_address', 'delivery_address']:
            f = self.__copyFixture()
            f[field].address = ""
            # Must raise exception
            with self.assertRaises(ValidationError) as cm:
                up = UserProfile(**f)
                up.full_clean()

            err = cm.exception
            self.assertIn(_(u"This field cannot be blank"), err.messages[0])


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(TestUserProfile)
