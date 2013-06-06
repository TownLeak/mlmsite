"""
Tests for accounts module. These will pass when you run "manage.py test".
"""
import unittest

import test_user
import test_userprofile
import test_signupform
import test_formfield_validators
import test_adult_birthday_field
import test_postal_address
import test_selenium


def suite():
    return unittest.TestSuite([
        test_user.TheTestSuite(),
        test_userprofile.TheTestSuite(),
        test_signupform.TheTestSuite(),
        test_formfield_validators.TheTestSuite(),
        test_adult_birthday_field.TheTestSuite(),
        test_postal_address.TheTestSuite(),
        test_selenium.TheTestSuite(),
    ])
