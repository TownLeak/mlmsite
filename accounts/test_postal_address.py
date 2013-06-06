from django.utils import unittest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from models import PostalAddress


class TestPostalAddress(TestCase):
    f_postal_address = {
        'address': "address1",
        'city': "City",
        'state': "State",
        'zip_code': "12345",
        'country': 'HU'
    }

    # -------------------------------------------------------------------------
    def testGoodCase(self):
        # Good case, must not raise
        pa = PostalAddress(**self.f_postal_address)
        pa.full_clean()

    # -------------------------------------------------------------------------
    def testBlanksMustRaise(self):
        for field in ['address', 'city', 'zip_code', 'country']:
            f = self.f_postal_address.copy()
            f[field] = ''
            pa = PostalAddress(**f)

            with self.assertRaises(ValidationError) as cm:
                pa.full_clean()

            err = cm.exception
            self.assertIn(_(u"This field cannot be blank"), err.messages[0])

    # -------------------------------------------------------------------------
    def testOptionalsShouldNotRaise(self):
        for field in ['state']:
            f = self.f_postal_address.copy()
            f[field] = ''
            pa = PostalAddress(**f)
            # Should not raise here
            pa.full_clean()

    # -------------------------------------------------------------------------
    def testCountry(self):
        pa = PostalAddress(**self.f_postal_address)
        pa.full_clean()
        self.assertEqual(pa.country.name, _(u"Hungary"))


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(TestPostalAddress)
