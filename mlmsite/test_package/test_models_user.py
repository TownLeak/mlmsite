import unittest
from django.test import TestCase
from mlmsite.models import User, MasterUser, UnilevelPosition


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

    def _testAddNewActiveUnilevelPosition_checks(self, user):
        self.assertTrue(user.active_unilevel_position)
        self.assertFalse(user.active_unilevel_position.parent)
        self.assertEqual(user.active_unilevel_position.__class__, UnilevelPosition)
        self.assertEqual(user.active_unilevel_position.id, user.active_unilevel_position.get_root().id)

    def testAddNewActiveUnilevelPosition(self):
        # User has no sponsor. In this case, the new active position must be
        # the tree top.
        user = User.objects.create(username="User")
        user.addNewActiveUnilevelPosition()
        self._testAddNewActiveUnilevelPosition_checks(user)
        # User has sponsor, but sponsor has no active position. In this case,
        # the new active position must be the tree top.
        sponsor = User.objects.create(username="Sponsor")
        user.sponsor = sponsor
        user.addNewActiveUnilevelPosition()
        self._testAddNewActiveUnilevelPosition_checks(user)
        # User has sponsor, and sponsor has active position. In this case, the parent
        # of the new position must be the active position of the sponsor.
        sponsor.addNewActiveUnilevelPosition()
        self._testAddNewActiveUnilevelPosition_checks(sponsor)
        user.addNewActiveUnilevelPosition()
        self.assertTrue(user.active_unilevel_position)
        self.assertEqual(user.active_unilevel_position.parent.id, sponsor.active_unilevel_position.id)
        self.assertEqual(user.active_unilevel_position.__class__, UnilevelPosition)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
