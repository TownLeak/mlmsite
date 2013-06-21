import unittest
from django.test import TestCase
from mlmsite.models import BinaryPosition, User


class Tests(TestCase):
    def test(self):
        pass


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
