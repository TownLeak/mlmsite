import unittest
from django.test import TestCase


class Tests(TestCase):
    def test(self):
        pass


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
