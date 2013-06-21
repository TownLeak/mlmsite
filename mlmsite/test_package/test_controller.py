import unittest
from django.test import TestCase
from mlmsite.controller import Controller
from mlmsite.binary_tree import BinaryTree
from mlmsite.unilevel_tree import UnilevelTree
from mlmsite.models import State, MasterUser, User, BinaryPosition, UnilevelPosition


class Tests(TestCase):
    def testInit(self):
        users = User.objects.all()
        self.assertFalse(users)
        states = State.objects.all()
        self.assertFalse(states)
        Controller()
        users = User.objects.all()
        self.assertEqual(1, len(users))
        master = users[0]
        self.assertTrue(master.isMaster())
        states = State.objects.all()
        self.assertEqual(1, len(states))
        self.assertTrue(states[0].actual_user.isMaster())
        self.assertEqual(master.binary_money, 0)
        self.assertEqual(master.id, master.id)

    def testGetActualUser(self):
        c = Controller()
        self.assertEqual(1, c.getActualUser().id)

    def testGetState(self):
        c = Controller()
        state = c._getState()
        self.assertEqual(state, State.objects.get(id=1))

    def testCreateNewBinaryPositionForUser(self):
        c = Controller()
        master = User.objects.get(id=1)
        user = User.objects.create(username="User", sponsor=master)
        self.assertEqual(1, len(BinaryPosition.objects.all()))
        self.assertFalse(user.active_binary_position)
        newPosition = c.createNewBinaryPosition(user)
        self.assertTrue(newPosition)
        self.assertEqual(newPosition, user.active_binary_position)
        self.assertEqual(2, len(BinaryPosition.objects.all()))
        self.assertEqual(master.active_binary_position.left, newPosition)
        self.assertEqual(newPosition.parent, master.active_binary_position)

    def _createBinaryPositions(self, numberOfPositions, sponsor):
        c = Controller()
        for i in range(0, numberOfPositions):
            user = User.objects.create(username=("User%d" % i), sponsor=sponsor)
            self.assertTrue(sponsor.active_binary_position)
            c.createNewBinaryPosition(user)

    def testHandleFullMatrixOfMaster(self):
        c = Controller()
        master = MasterUser.Get()
        logic = BinaryTree()
        numberOfUsers = logic._getNumberOfNodesToReturn() - 2
        self._createBinaryPositions(numberOfUsers, master)
        master = MasterUser.Get()
        self.assertEqual(numberOfUsers * c.price, master.binary_money)
        user = User.objects.create(username="Last User", sponsor=master)
        c.createNewBinaryPosition(user)
        # With this move, the master's matrix got full. Master should not get commission,
        # only the fees.
        master = MasterUser.Get()
        self.assertEqual((numberOfUsers + 1) * c.price, master.binary_money)
        # Check if the new position for the master has been created.
        # It must be a completely new matrix.
        self.assertEqual(master.active_binary_position.parent, None)

    def testHandleFullMatrixOfUser(self):
        c = Controller()
        master = MasterUser.Get()
        activeId = master.active_binary_position.id
        self.assertTrue(master.active_binary_position)
        self.assertEqual(master.id, 1)
        parentUser = User.objects.create(username="First User", sponsor=master)
        c.createNewBinaryPosition(parentUser)
        self.assertTrue(parentUser.active_binary_position)
        logic = BinaryTree()
        numberOfUsers = logic._getNumberOfNodesToReturn() - 2
        self._createBinaryPositions(numberOfUsers, parentUser)
        self.assertEqual(- c.price, parentUser.binary_money)
        last_user = User.objects.create(username="Last User", sponsor=parentUser)
        self.assertEqual(activeId, master.active_binary_position.id)
        self.assertEqual(last_user.sponsor.id, parentUser.id)
        c.createNewBinaryPosition(last_user)
        self.assertEqual(last_user.sponsor.id, parentUser.id)
        self.assertEqual(activeId, master.active_binary_position.id)
        master = MasterUser.Get()
        self.assertEqual((numberOfUsers + 2) * c.price - c.commission, master.binary_money)
        # With this move, the master's matrix got full. Sponsor should get commission, no new fee
        # should be paid after the repositioning.
        self.assertEqual(c.commission - c.price, parentUser.binary_money)
        # Check if the new position for the master has been created.
        # It must be the rightmost node at one level below the full matrix.
        self.assertEqual(parentUser.active_binary_position.parent.owner.id, master.id)
        self.assertTrue(master.active_binary_position.right)
        self.assertEqual(master.active_binary_position.right.id, parentUser.active_binary_position.id)

    def testSetActualUser(self):
        c = Controller()
        newUser = User.CreateNewUser(User.objects.get(id=1))
        self.assertNotEqual(newUser, c.getActualUser())
        c.setActualUser(newUser)
        self.assertEqual(newUser, c.getActualUser())

    def testPayFee(self):
        c = Controller()
        master = MasterUser.Get()
        user = User.objects.create(username="Last User", sponsor=master)
        self.assertEqual(0, user.binary_money)
        self.assertEqual(0, master.binary_money)
        c.payFee(user)
        self.assertEqual(-c.price, user.binary_money)
        master = MasterUser.Get()
        self.assertEqual(c.price, master.binary_money)

    def testPayCommission(self):
        c = Controller()
        master = MasterUser.Get()
        user = User.objects.create(username="Last User", sponsor=master)
        self.assertEqual(0, user.binary_money)
        c.payCommission(user)
        master = MasterUser.Get()
        self.assertEqual(c.commission, user.binary_money)
        self.assertEqual(-c.commission, master.binary_money)

    def testUserLeaves_MasterCannotLeave(self):
        c = Controller()
        master = MasterUser.Get()
        with self.assertRaises(MasterUser.MasterCannotLeave):
            c.userLeaves(master)
        user1 = User.objects.create(username="user1", sponsor=master)
        user2 = User.objects.create(username="user2", sponsor=user1)
        self.assertEqual(user2.sponsor.id, user1.id)
        id = user2.id
        self.assertTrue(user1.isActive)
        c.userLeaves(user1)
        self.assertFalse(user1.isActive)
        user2 = User.objects.get(id=id)
        self.assertEqual(user2.sponsor.id, master.id)

    def testCreateNewUser(self):
        c = Controller()
        c._getState().tree_view = State.UNILEVEL_TREE
        master = MasterUser.Get()
        user1 = c.createNewUser(master)
        tree = UnilevelTree()
        tree.treeToJson(user1.active_unilevel_position)
        user2 = c.createNewUser(user1)
        tree.treeToJson(user1.active_unilevel_position)
        tree.treeToJson(user2.active_unilevel_position)

    def testCalculateMonthlyCommission(self):
        c = Controller()
        self.assertEqual(c.monthly_fee, 100)
        self.assertEqual(c.monthly_percent, 10)
        self.assertEqual(c.calculateMonthlyCommission(), 10)

    def testPayMonthlyCommission(self):
        c = Controller()
        user = User.objects.create(username="User")
        user.addNewActiveUnilevelPosition()
        position_1_1 = UnilevelPosition.objects.create(owner=user, parent=user.active_unilevel_position)
        position_1_1.save()
        self.assertEqual(user.unilevel_money, 0)
        c.payMonthlyCommission(user)
        self.assertEqual(user.unilevel_money, 10)
        position_1_2 = UnilevelPosition.objects.create(owner=user, parent=user.active_unilevel_position)
        position_1_2.save()
        c.payMonthlyCommission(user)
        self.assertEqual(user.unilevel_money, 30)

    def testExecuteMonthlyPayments_MasterReceivesNoPayment(self):
        master = MasterUser.Get()
        c = Controller()
        self.assertEqual(0, master.unilevel_money)
        c.executeMonthlyPayments()
        self.assertEqual(0, master.unilevel_money)

    def _createInvitedUser(self, sponsor):
        user = User.CreateNewUser(sponsor=sponsor)
        user.addNewActiveUnilevelPosition()
        return user

    def testExecuteMonthlyPayments_UserReceivesPayment(self):
        master = MasterUser.Get()
        c = Controller()
        user1 = self._createInvitedUser(sponsor=master)
        id1 = user1.id
        c.executeMonthlyPayments()
        user1 = User.objects.get(id=id1)
        master = MasterUser.Get()
        self.assertEqual(100, master.unilevel_money)
        self.assertEqual(-100, user1.unilevel_money)
        user2 = self._createInvitedUser(sponsor=user1)
        id2 = user2.id
        self.assertEqual(0, user2.binary_money)
        self.assertEqual(0, user2.unilevel_money)
        c.executeMonthlyPayments()
        user1 = User.objects.get(id=id1)
        user2 = User.objects.get(id=id2)
        master = MasterUser.Get()
        self.assertEqual(0, master.binary_money)
        self.assertEqual(290, master.unilevel_money)
        self.assertEqual(0, user1.binary_money)
        self.assertEqual(-190, user1.unilevel_money)
        self.assertEqual(0, user2.binary_money)
        self.assertEqual(-100, user2.unilevel_money)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
