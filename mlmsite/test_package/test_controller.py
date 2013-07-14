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
        userId = User.objects.create(username="User", sponsor=MasterUser.Get()).id
        self.assertEqual(1, len(BinaryPosition.objects.all()))
        self.assertFalse(User.Get(userId).active_binary_position)
        newPosition = Controller().createNewBinaryPosition(userId)
        self.assertTrue(newPosition)
        self.assertEqual(newPosition, User.Get(userId).active_binary_position)
        self.assertEqual(2, len(BinaryPosition.objects.all()))
        self.assertEqual(MasterUser.Get().active_binary_position.left, newPosition)
        self.assertEqual(newPosition.parent, MasterUser.Get().active_binary_position)

    def _createBinaryPositions(self, numberOfPositions, sponsorId):
        for i in range(0, numberOfPositions):
            user = User.objects.create(username=("User%d" % i), sponsor=User.Get(sponsorId))
            self.assertTrue(User.Get(sponsorId).active_binary_position)
            Controller().createNewBinaryPosition(user.id)

    def testHandleFullMatrixOfMaster(self):
        numberOfUsers = BinaryTree()._getNumberOfNodesToReturn() - 2
        self._createBinaryPositions(numberOfUsers, MasterUser.Get().id)
        self.assertEqual(numberOfUsers * Controller().price, MasterUser.Get().binary_money)
        user = User.objects.create(username="Last User", sponsor=MasterUser.Get())
        Controller().createNewBinaryPosition(user.id)
        # With this move, the master's matrix got full. Master should not get commission,
        # only the fees.
        self.assertEqual((numberOfUsers + 1) * Controller().price, MasterUser.Get().binary_money)
        # Check if the new position for the master has been created.
        # It must be a completely new matrix.
        self.assertEqual(MasterUser.Get().active_binary_position.parent, None)

    def testHandleFullMatrixOfUser(self):
        activeId = MasterUser.Get().active_binary_position.id
        self.assertTrue(MasterUser.Get().active_binary_position)
        self.assertEqual(MasterUser.Get().id, 1)
        parentUserId = User.objects.create(username="First User", sponsor=MasterUser.Get()).id
        Controller().createNewBinaryPosition(parentUserId)
        self.assertTrue(User.Get(parentUserId).active_binary_position)
        numberOfUsers = BinaryTree()._getNumberOfNodesToReturn() - 2
        self._createBinaryPositions(numberOfUsers, parentUserId)
        self.assertEqual(- Controller().price, User.Get(parentUserId).binary_money)
        lastUserId = User.objects.create(username="Last User", sponsor=User.Get(parentUserId)).id
        self.assertEqual(activeId, MasterUser.Get().active_binary_position.id)
        self.assertEqual(User.Get(lastUserId).sponsor.id, parentUserId)
        Controller().createNewBinaryPosition(lastUserId)
        self.assertEqual(User.Get(lastUserId).sponsor.id, parentUserId)
        self.assertEqual(activeId, MasterUser.Get().active_binary_position.id)
        self.assertEqual((numberOfUsers + 2) * Controller().price - Controller().commission, MasterUser.Get().binary_money)
        # With this move, the parent's matrix got full. Sponsor should get commission, no new fee
        # should be paid after the repositioning.
        # This line has been failed. Test0002 was used for debugging.
        self.assertEqual(- Controller().price + Controller().commission, User.Get(parentUserId).binary_money)
        # Check if the new position for the master has been created.
        # It must be the rightmost node at one level below the full matrix.
        self.assertEqual(User.Get(parentUserId).active_binary_position.parent.owner.id, MasterUser.Get().id)
        self.assertTrue(MasterUser.Get().active_binary_position.right)
        self.assertEqual(MasterUser.Get().active_binary_position.right.id, User.Get(parentUserId).active_binary_position.id)

    def testTest0002(self):
        """It turned out that binary comission was not paid for user when a binary matrix got full.
           in testHandleFullMatrixOfUser. In this test, we go to the failure point and execute the test
           function line-by-line."""
        parentUserId = User.objects.create(username="First User", sponsor=MasterUser.Get()).id
        Controller().createNewBinaryPosition(parentUserId)
        numberOfUsers = BinaryTree()._getNumberOfNodesToReturn() - 2
        self._createBinaryPositions(numberOfUsers, parentUserId)
        lastUserId = User.objects.create(username="Last User", sponsor=User.Get(parentUserId)).id
        # This was the failed line:
        # Controller().createNewBinaryPosition(lastUserId)
        self.assertTrue(User.Get(lastUserId).addNewActiveBinaryPosition())
        # Check situation before payment
        self.assertEqual(- Controller().price, User.Get(parentUserId).binary_money)
        Controller().payBinaryPrice(lastUserId)
        self.assertEqual(- Controller().price, User.Get(parentUserId).binary_money)
        # This line did noy pay commision for parent user. Extend it, check line-by-line
        # Controller()._handleFullMatrix(User.Get(lastUserId).active_binary_position)
        position = User.Get(lastUserId).active_binary_position
        top = BinaryTree().getMatrixTop(position)
        self.assertTrue(not top.owner.isMaster())
        if not top.owner.isMaster():
            Controller().payBinaryCommission(top.owner.id)
        # OK, this was the error. payBinaryCommission was called, saved the new money state,
        # but this line re-saved the old state.
        # top.owner.save()
        self.assertEqual(- Controller().price + Controller().commission, User.Get(parentUserId).binary_money)

    def testSetActualUser(self):
        c = Controller()
        newUser = User.CreateNewUser(User.objects.get(id=1))
        self.assertNotEqual(newUser, c.getActualUser())
        c.setActualUser(newUser)
        self.assertEqual(newUser, c.getActualUser())

    def testPayBinaryPrice(self):
        userId = User.objects.create(username="Last User", sponsor=MasterUser.Get()).id
        self.assertEqual(0, User.Get(userId).binary_money)
        self.assertEqual(0, MasterUser.Get().binary_money)
        Controller().payBinaryPrice(userId)
        self.assertEqual(-Controller().price, User.Get(userId).binary_money)
        self.assertEqual(Controller().price, MasterUser.Get().binary_money)

    def testPayBinaryCommission(self):
        userId = User.objects.create(username="Last User", sponsor=MasterUser.Get()).id
        self.assertEqual(0, User.Get(userId).binary_money)
        Controller().payBinaryCommission(userId)
        self.assertEqual(Controller().commission, User.Get(userId).binary_money)
        self.assertEqual(-Controller().commission, MasterUser.Get().binary_money)

    def testUserLeaves_MasterCannotLeave(self):
        c = Controller()
        with self.assertRaises(MasterUser.MasterCannotLeave):
            c.userLeaves(MasterUser.Get().id)
        user1Id = User.objects.create(username="user1", sponsor=MasterUser.Get()).id
        user2Id = User.objects.create(username="user2", sponsor=User.Get(user1Id)).id
        self.assertEqual(User.Get(user2Id).sponsor.id, user1Id)
        self.assertTrue(User.Get(user1Id).isActive)
        c.userLeaves(user1Id)
        self.assertFalse(User.Get(user1Id).isActive)
        self.assertEqual(User.Get(user2Id).sponsor.id, MasterUser.Get().id)

    def testCreateNewUser(self):
        c = Controller()
        c._getState().tree_view = State.UNILEVEL_TREE
        master = MasterUser.Get()
        user1Id = c.createNewUser(master)
        tree = UnilevelTree()
        tree.treeToJson(User.Get(user1Id).active_unilevel_position)
        user2Id = c.createNewUser(User.Get(user1Id))
        tree.treeToJson(User.Get(user1Id).active_unilevel_position)
        tree.treeToJson(User.Get(user2Id).active_unilevel_position)

    def testCreateNewUser_persistency(self):
        self.assertTrue(User.Get(Controller().createNewUser(MasterUser.Get())).active_unilevel_position)

    def testCalculateMonthlyCommission(self):
        c = Controller()
        self.assertEqual(c.monthly_fee, 100)
        self.assertEqual(c.monthly_percent, 10)
        self.assertEqual(c.calculateMonthlyCommission(), 10)

    def testPayMonthlyCommission(self):
        userId = User.objects.create(username="User").id
        User.Get(userId).addNewActiveUnilevelPosition()
        position_1_1 = UnilevelPosition.objects.create(owner=User.Get(userId), parent=User.Get(userId).active_unilevel_position)
        position_1_1.save()
        self.assertEqual(User.Get(userId).unilevel_money, 0)
        Controller().payMonthlyCommission(userId)
        self.assertEqual(User.Get(userId).unilevel_money, 10)
        position_1_2 = UnilevelPosition.objects.create(owner=User.Get(userId), parent=User.Get(userId).active_unilevel_position)
        position_1_2.save()
        Controller().payMonthlyCommission(userId)
        self.assertEqual(User.Get(userId).unilevel_money, 30)

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
        user1 = self._createInvitedUser(sponsor=master)
        id1 = user1.id
        Controller().executeMonthlyPayments()
        user1 = User.objects.get(id=id1)
        master = MasterUser.Get()
        self.assertEqual(100, master.unilevel_money)
        self.assertEqual(-100, user1.unilevel_money)
        user2 = self._createInvitedUser(sponsor=user1)
        id2 = user2.id
        self.assertEqual(0, user2.binary_money)
        self.assertEqual(0, user2.unilevel_money)
        Controller().executeMonthlyPayments()
        user1 = User.objects.get(id=id1)
        user2 = User.objects.get(id=id2)
        master = MasterUser.Get()
        self.assertEqual(0, master.binary_money)
        self.assertEqual(290, master.unilevel_money)
        self.assertEqual(0, user1.binary_money)
        self.assertEqual(-190, user1.unilevel_money)
        self.assertEqual(0, user2.binary_money)
        self.assertEqual(-100, user2.unilevel_money)

    def _getFirstOrdinaryUser(self):
        return User.objects.get(id=User.IdOfFirstOrdinaryUser())

    def testOneFullMatrix(self):
        self.assertEqual(BinaryTree._levelsOfFullMatrix, 3)

        # Create six users: master's first matrix runs out
        for i in range(6):
            Controller().createNewUser(MasterUser.Get())

        self.assertFalse(MasterUser.Get().active_binary_position.left)
        self.assertEqual(6 * Controller.price, MasterUser.Get().binary_money)

        # Create four users: user1's first matrix is over
        for i in range(4):
            Controller().createNewUser(self._getFirstOrdinaryUser())

        self.assertFalse(self._getFirstOrdinaryUser().active_binary_position.left)
        self.assertEqual(self._getFirstOrdinaryUser().active_binary_position.parent.owner.id, MasterUser.Get().id)
        # This line did not pass. A separate test had been done, test id: Test0001
        # Problem was: we did not use MasterUser.Get(), to get the actual master object, so
        # master variable reflected an earlier state.
        self.assertTrue(MasterUser.Get().active_binary_position.left)
        self.assertTrue(self._getFirstOrdinaryUser().active_binary_position.parent)
        self.assertEqual(MasterUser.Get().active_binary_position.left.id, self._getFirstOrdinaryUser().active_binary_position.id)

    def testTestId0001(self):
        """Assuming matrix depth 3, we create 6 users for master, then 4 for user1. The following must be true:
           - Master matrix runs out
           - at the last creation, user1 must run out
           - User 1's new position is the left child of master's actual position
           - Commissions has been played properly"""
        self.assertEqual(BinaryTree._levelsOfFullMatrix, 3)
        oldMasterPositionId = MasterUser.Get().active_binary_position.id
        # Create six users for master - master runs out (not checked)
        for i in range(6):
            Controller().createNewUser(MasterUser.Get())
        # Create three users: user1's first matrix is not yet over. Test if all the conditions are OK here,
        # before we create another user sponsored by user1 (so that user1 runs out)
        for i in range(3):
            Controller().createNewUser(self._getFirstOrdinaryUser())

        self.assertEqual(-Controller().price, self._getFirstOrdinaryUser().binary_money)
        self.assertEqual(9 * Controller().price, MasterUser.Get().binary_money)
        self.assertEqual(self._getFirstOrdinaryUser().active_binary_position.parent.id, oldMasterPositionId)
        newMasterPositionId = MasterUser.Get().active_binary_position.id
        self.assertNotEqual(newMasterPositionId, oldMasterPositionId)
        self.assertFalse(MasterUser.Get().active_binary_position.left)
        self.assertFalse(MasterUser.Get().active_binary_position.right)

        # Now, create another user, sponsorred by user1. User1 must run out.
        oldUser1PositionId = self._getFirstOrdinaryUser().active_binary_position.id
        Controller().createNewUser(self._getFirstOrdinaryUser())
        newUser1PositionId = self._getFirstOrdinaryUser().active_binary_position.id
        self.assertNotEqual(newUser1PositionId, oldUser1PositionId)
        self.assertTrue(MasterUser.Get().active_binary_position.left)
        self.assertEqual(MasterUser.Get().active_binary_position.left.id, newUser1PositionId)
        # Here, commission should be paid for user1, that is 2 * the price. Som master's mani is less...
        self.assertEqual(MasterUser.Get().binary_money, (10 - 2) * Controller().price)
        self.assertEqual(self._getFirstOrdinaryUser().binary_money, Controller().price)

    def testCreateMoreNewUsers_2(self):
        self.assertEqual(BinaryTree._levelsOfFullMatrix, 3)
        Controller().createMoreNewUsers(2)
        self.assertEqual(MasterUser.Get().active_binary_position.left.id, 2)
        self.assertEqual(MasterUser.Get().active_binary_position.right.id, 3)

    def testCreateMoreNewUsers_6(self):
        self.assertEqual(BinaryTree._levelsOfFullMatrix, 3)
        Controller().createMoreNewUsers(6)
        self.assertFalse(MasterUser.Get().active_binary_position.left)
        self.assertFalse(MasterUser.Get().active_binary_position.right)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
