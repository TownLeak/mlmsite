import unittest
from django.test import TestCase
from mlmsite.models import User, MasterUser


class Tests(TestCase):
    def testLeave(self):
        user = User.objects.create(username="User")
        self.assertTrue(user.isActive)
        user.leave()
        self.assertFalse(user.isActive)
        master = MasterUser.Get()
        self.assertTrue(master.isActive)
        with self.assertRaises(User.MasterCannotLeave):
            master.leave()
        self.assertTrue(master.isActive)

    def testCreateNewUser(self):
        self.assertEqual(0, len(User.objects.all()))
        sponsor = MasterUser.Get()
        newUser = User.CreateNewUser(sponsor)
        self.assertEqual(2, len(User.objects.all()))
        self.assertEqual("user1", newUser.username)
        self.assertEqual(sponsor.id, newUser.sponsor.id)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
