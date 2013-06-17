import unittest
from django.test import TestCase
from mlmsite.controller import Controller
from mlmsite.binary_tree import BinaryTree
from mlmsite.models import MasterUser, User, BinaryPosition


class Tests(TestCase):
    def testInit(self):
        users = Controller.user_type.objects.all()
        self.assertFalse(users)
        states = Controller.state_type.objects.all()
        self.assertFalse(states)
        Controller()
        users = Controller.user_type.objects.all()
        self.assertEqual(1, len(users))
        master = users[0]
        self.assertTrue(master.isMaster())
        states = Controller.state_type.objects.all()
        self.assertEqual(1, len(states))
        self.assertTrue(states[0].actual_user.isMaster())
        self.assertEqual(master.money, 0)
        self.assertEqual(master.id, master.id)

    def testGetState(self):
        c = Controller()
        state = c._getState()
        self.assertEqual(state, Controller.state_type.objects.get(id=1))

    def testGetActualData(self):
        c = Controller()
        nodes = c.getActualData()
        self.assertEqual(7, len(nodes))
        self.assertEqual(nodes[0], BinaryPosition.objects.get(id=1))

    def testCreateNewBinaryPositionForUser(self):
        c = Controller()
        master = Controller.user_type.objects.get(id=1)
        user = Controller.user_type.objects.create(username="User", sponsor=master)
        self.assertEqual(1, len(BinaryPosition.objects.all()))
        self.assertFalse(user.active_binary_position)
        newPosition = c.createNewBinaryPosition(user)
        self.assertTrue(newPosition)
        self.assertEqual(newPosition, user.active_binary_position)
        self.assertEqual(2, len(BinaryPosition.objects.all()))
        self.assertEqual(master.active_binary_position.left, newPosition)
        self.assertEqual(newPosition.top, master.active_binary_position)

    def _createBinaryPositions(self, numberOfPositions, sponsor):
        c = Controller()
        for i in range(0, numberOfPositions):
            user = Controller.user_type.objects.create(username=("User%d" % i), sponsor=sponsor)
            self.assertTrue(sponsor.active_binary_position)
            c.createNewBinaryPosition(user)

    def testHandleFullMatrixOfMaster(self):
        c = Controller()
        master = MasterUser.Get()
        logic = BinaryTree()
        numberOfUsers = logic._getNumberOfNodesToReturn() - 2
        self._createBinaryPositions(numberOfUsers, master)
        master = MasterUser.Get()
        self.assertEqual(numberOfUsers * c.price, master.money)
        user = Controller.user_type.objects.create(username="Last User", sponsor=master)
        c.createNewBinaryPosition(user)
        # With this move, the master's matrix got full. Master should not get commission,
        # only the fees.
        master = MasterUser.Get()
        self.assertEqual((numberOfUsers + 1) * c.price, master.money)
        # Check if the new position for the master has been created.
        # It must be a completely new matrix.
        self.assertEqual(master.active_binary_position.top, None)

    def testHandleFullMatrixOfUser(self):
        c = Controller()
        master = MasterUser.Get()
        activeId = master.active_binary_position.id
        self.assertTrue(master.active_binary_position)
        self.assertEqual(master.id, 1)
        topUser = Controller.user_type.objects.create(username="First User", sponsor=master)
        c.createNewBinaryPosition(topUser)
        self.assertTrue(topUser.active_binary_position)
        logic = BinaryTree()
        numberOfUsers = logic._getNumberOfNodesToReturn() - 2
        self._createBinaryPositions(numberOfUsers, topUser)
        self.assertEqual(- c.price, topUser.money)
        last_user = Controller.user_type.objects.create(username="Last User", sponsor=topUser)
        self.assertEqual(activeId, master.active_binary_position.id)
        self.assertEqual(last_user.sponsor.id, topUser.id)
        c.createNewBinaryPosition(last_user)
        self.assertEqual(last_user.sponsor.id, topUser.id)
        self.assertEqual(activeId, master.active_binary_position.id)
        master = MasterUser.Get()
        self.assertEqual((numberOfUsers + 2) * c.price - c.commission, master.money)
        # With this move, the master's matrix got full. Sponsor should get commission, no new fee
        # should be paid after the repositioning.
        self.assertEqual(c.commission - c.price, topUser.money)
        # Check if the new position for the master has been created.
        # It must be the rightmost node at one level below the full matrix.
        self.assertEqual(topUser.active_binary_position.top.owner.id, master.id)
        self.assertTrue(master.active_binary_position.right)
        self.assertEqual(master.active_binary_position.right.id, topUser.active_binary_position.id)

    def testSetActualUser(self):
        c = Controller()
        newUser = User.CreateNewUser(Controller.user_type.objects.get(id=1))
        self.assertNotEqual(newUser, c.getActualUser())
        c.setActualUser(newUser)
        self.assertEqual(newUser, c.getActualUser())

    def testPayFee(self):
        c = Controller()
        master = MasterUser.Get()
        user = Controller.user_type.objects.create(username="Last User", sponsor=master)
        self.assertEqual(0, user.money)
        self.assertEqual(0, master.money)
        c.payFee(user)
        self.assertEqual(-c.price, user.money)
        master = MasterUser.Get()
        self.assertEqual(c.price, master.money)

    def testPayCommission(self):
        c = Controller()
        master = MasterUser.Get()
        user = Controller.user_type.objects.create(username="Last User", sponsor=master)
        self.assertEqual(0, user.money)
        c.payCommission(user)
        master = MasterUser.Get()
        self.assertEqual(c.commission, user.money)
        self.assertEqual(-c.commission, master.money)

    def testUserLeaves_MasterCannotLeave(self):
        c = Controller()
        master = MasterUser.Get()
        with self.assertRaises(MasterUser.MasterCannotLeave):
            c.userLeaves(master)
        user1 = Controller.user_type.objects.create(username="user1", sponsor=master)
        user2 = Controller.user_type.objects.create(username="user2", sponsor=user1)
        self.assertEqual(user2.sponsor.id, user1.id)
        id = user2.id
        self.assertTrue(user1.isActive)
        c.userLeaves(user1)
        self.assertFalse(user1.isActive)
        user2 = Controller.user_type.objects.get(id=id)
        self.assertEqual(user2.sponsor.id, master.id)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
