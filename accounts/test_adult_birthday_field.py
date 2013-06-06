import datetime

from django.utils import unittest
from django.test import TestCase
from django.utils.translation import ugettext as _
from models import AdultBirthDateField, AgeError
from config import Config


class MockDateTimeFactory:
    def getToday(self):
        return datetime.date(2010, 1, 2)


class MockMinAgeFactory:
    def getMinAge(self):
        return 10


class MockDependencies:
    dateTimeFactory = MockDateTimeFactory()
    minAgeFactory = MockMinAgeFactory()


class TestAdultBirthDateField(TestCase):
    """
    Test AdultBirtdDayField object.
    """

    # -------------------------------------------------------------------------
    def testDefaultFactories(self):
        f = AdultBirthDateField()
        self.assertEqual(datetime.date.today(), f.deps.dateTimeFactory.getToday())
        self.assertEqual(Config.min_age, f.deps.minAgeFactory.getMinAge())

    # -------------------------------------------------------------------------
    def testMockFactories(self):
        f = AdultBirthDateField(deps=MockDependencies())
        self.assertEqual(datetime.date(2010, 1, 2), f.deps.dateTimeFactory.getToday())
        self.assertEqual(10, f.deps.minAgeFactory.getMinAge())

    # -------------------------------------------------------------------------
    def testAgeError(self):
        err = AgeError(deps=MockDependencies())
        self.assertEqual([_(u"You must be min 10 years old.")], err.messages)

    # -------------------------------------------------------------------------
    def testIsAdultValidator(self):
        # Check (min_age + 1) years old - must pass
        bd = datetime.date(1999, 01, 02)
        obj = AdultBirthDateField(deps=MockDependencies())

        # Check (min_age - 1) years old: must fail
        bd = datetime.date(2001, 01, 02)
        obj = AdultBirthDateField(deps=MockDependencies())

        with self.assertRaises(AgeError):
            obj.isAdultValidator(bd)

        # Check min_age + 1 day: must pass
        bd = datetime.date(2000, 01, 01)
        obj = AdultBirthDateField(deps=MockDependencies())

        # Check min_age - 1 day: must fail
        bd = datetime.date(2001, 01, 03)
        obj = AdultBirthDateField(deps=MockDependencies())

        with self.assertRaises(AgeError):
            obj.isAdultValidator(bd)

        # Check that user today gets adult: must pass
        bd = datetime.date(2001, 01, 02)
        obj = AdultBirthDateField(deps=MockDependencies())

    # -------------------------------------------------------------------------
    def testAdultBirthDateFieldInit(self):
        f = AdultBirthDateField()
        self.assertEqual(_(u'Birth date'), f.verbose_name)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(TestAdultBirthDateField)
