import unittest
from django.test import TestCase
from mlmsite.models import GraphEval_User as User


class Tests(TestCase):
    def testIsMaster(self):
        master = User.objects.create(username="Master")
        self.assertTrue(master.isMaster())
        user = User.objects.create(username="Last User", sponsor=master)
        self.assertFalse(user.isMaster())

    def testLeave(self):
        user = User.objects.create(username="Last User")
        self.assertTrue(user.isActive)
        user.leave()
        self.assertFalse(user.isActive)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
