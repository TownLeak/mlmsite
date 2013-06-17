import unittest
from django.test import TestCase
from mlmsite.tree import Tree


class Tests(TestCase):
    def test(self):
        pass


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
