import unittest
from django.test import TestCase
from mlmsite.unilevel_tree import UnilevelTree


class Tests(TestCase):
    def test(self):
        pass


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
