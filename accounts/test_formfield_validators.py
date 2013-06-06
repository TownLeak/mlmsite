
from django.utils import unittest
from django.test import TestCase

from django import forms


class TestFormFieldValidators(TestCase):
    def testEmailField(self):
        self.assertFieldOutput(forms.EmailField,
            {'a@a.com': 'a@a.com'},
            {'aaa': [u'Enter a valid e-mail address.']})


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(TestFormFieldValidators)
