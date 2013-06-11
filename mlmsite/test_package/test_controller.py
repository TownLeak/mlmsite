import unittest
from django.test import TestCase
from mlmsite.controller import Controller
from mlmsite.binary_tree_logic import BinaryTreeLogic


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
        self.assertEqual(master.username, Controller.conf_master_username)
        states = Controller.state_type.objects.all()
        self.assertEqual(1, len(states))
        self.assertEqual(states[0].actual_user.username, Controller.conf_master_username)
        self.assertEqual(master.money, 0)
        self.assertEqual(master.id, master.sponsor.id)

    def testGetState(self):
        c = Controller()
        state = c._getState()
        self.assertEqual(state, Controller.state_type.objects.get(id=1))

    def testGetActualData(self):
        c = Controller()
        nodes = c.getActualData()
        self.assertEqual(7, len(nodes))
        self.assertEqual(nodes[0], Controller.position_type.objects.get(id=1))

    def testCreateNewUser(self):
        c = Controller()
        self.assertEqual(1, len(Controller.user_type.objects.all()))
        sponsor = Controller.user_type.objects.get(id=1)
        newUser = c.createNewUser(sponsor)
        self.assertEqual(2, len(Controller.user_type.objects.all()))
        self.assertEqual("user1", newUser.username)
        self.assertEqual(sponsor, newUser.sponsor)

    def testCreateNewPositionForUser(self):
        c = Controller()
        master = Controller.user_type.objects.get(id=1)
        user = Controller.user_type.objects.create(username="User", sponsor=master)
        self.assertEqual(1, len(Controller.position_type.objects.all()))
        self.assertFalse(user.active_position)
        newPosition = c.createNewPosition(user)
        self.assertTrue(newPosition)
        self.assertEqual(newPosition, user.active_position)
        self.assertEqual(2, len(Controller.position_type.objects.all()))
        self.assertEqual(master.active_position.left_guy, newPosition)
        self.assertEqual(newPosition.sponsor, master.active_position)

    def _createPositions(self, numberOfPositions, sponsor):
        c = Controller()
        for i in range(0, numberOfPositions):
            user = Controller.user_type.objects.create(username=("User%d" % i), sponsor=sponsor)
            self.assertTrue(sponsor.active_position)
            c.createNewPosition(user)

    def testHandleFullMatrixOfMaster(self):
        c = Controller()
        master = c.getMaster()
        logic = BinaryTreeLogic()
        numberOfUsers = logic._getNumberOfNodesToReturn() - 2
        self._createPositions(numberOfUsers, master)
        master = c.getMaster()
        self.assertEqual(numberOfUsers * c.price, master.money)
        user = Controller.user_type.objects.create(username="Last User", sponsor=master)
        c.createNewPosition(user)
        # With this move, the master's matrix got full. Master should not get commission,
        # only the fees.
        master = c.getMaster()
        self.assertEqual((numberOfUsers + 1) * c.price, master.money)
        # Check if the new position for the master has been created.
        # It must be a completely new matrix.
        self.assertEqual(master.active_position.sponsor, None)

    def testHandleFullMatrixOfUser(self):
        c = Controller()
        master = c.getMaster()
        activeId = master.active_position.id
        self.assertTrue(master.active_position)
        self.assertEqual(master.id, 1)
        topUser = Controller.user_type.objects.create(username="First User", sponsor=master)
        c.createNewPosition(topUser)
        self.assertTrue(topUser.active_position)
        logic = BinaryTreeLogic()
        numberOfUsers = logic._getNumberOfNodesToReturn() - 2
        self._createPositions(numberOfUsers, topUser)
        self.assertEqual(- c.price, topUser.money)
        last_user = Controller.user_type.objects.create(username="Last User", sponsor=topUser)
        self.assertEqual(activeId, master.active_position.id)
        self.assertEqual(last_user.sponsor.id, topUser.id)
        c.createNewPosition(last_user)
        self.assertEqual(last_user.sponsor.id, topUser.id)
        self.assertEqual(activeId, master.active_position.id)
        master = c.getMaster()
        self.assertEqual((numberOfUsers + 2) * c.price - c.commission, master.money)
        # With this move, the master's matrix got full. Sponsor should get commission, no new fee
        # should be paid after the repositioning.
        self.assertEqual(c.commission - c.price, topUser.money)
        # Check if the new position for the master has been created.
        # It must be the rightmost node at one level below the full matrix.
        self.assertEqual(topUser.active_position.sponsor.user.id, master.id)
        self.assertTrue(master.active_position.right_guy)
        self.assertEqual(master.active_position.right_guy.id, topUser.active_position.id)

    def testSetActualUser(self):
        c = Controller()
        newUser = c.createNewUser(Controller.user_type.objects.get(id=1))
        self.assertNotEqual(newUser, c.getActualUser())
        c.setActualUser(newUser)
        self.assertEqual(newUser, c.getActualUser())

    def testPayFee(self):
        c = Controller()
        master = c.getMaster()
        user = Controller.user_type.objects.create(username="Last User", sponsor=master)
        self.assertEqual(0, user.money)
        self.assertEqual(0, master.money)
        c.payFee(user)
        self.assertEqual(-c.price, user.money)
        master = c.getMaster()
        self.assertEqual(c.price, master.money)

    def testGetMaster(self):
        c = Controller()
        master = c.getMaster()
        self.assertEqual(master.username, c.conf_master_username)

    def testPayCommission(self):
        c = Controller()
        master = c.getMaster()
        user = Controller.user_type.objects.create(username="Last User", sponsor=master)
        self.assertEqual(0, user.money)
        c.payCommission(user)
        master = c.getMaster()
        self.assertEqual(c.commission, user.money)
        self.assertEqual(-c.commission, master.money)

    def testIsMaster(self):
        c = Controller()
        master = c.getMaster()
        self.assertTrue(c.isMaster(master))
        user = Controller.user_type.objects.create(username="Last User", sponsor=master)
        self.assertFalse(c.isMaster(user))


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
