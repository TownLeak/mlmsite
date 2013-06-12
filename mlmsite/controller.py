#!/usr/bin/python
# -*- coding: utf-8
from models import GraphEval_User as User
from models import GraphEval_Position as Position
from models import GraphEval_State as State
from binary_tree_logic import BinaryTreeLogic
from position_manager import PositionManager


class Controller:
    price = 100
    commission = 2 * price

    class LogicError(Exception):
        pass

    class MasterCannotLeave(Exception):
        pass

    user_type = User
    state_type = State
    position_type = Position
    conf_master_username = "A Mester"
    conf_binary_matrix_display_depth = 3

    def __init__(self):
        if not User.objects.all():
            master = User.objects.create(username=self.conf_master_username)
            position = Position.objects.create(name="Position0", user=master)
            master.active_position = position
            master.sponsor = master
            master.money = 0
            master.save()
        else:
            master = User.objects.get(username=self.conf_master_username)

        if not State.objects.all():
            State.objects.create(actual_user=master)

    def _getState(self):
        return State.objects.get(id=1)

    def getActualUser(self):
        return self._getState().actual_user

    def getActualData(self):
        state = self._getState()
        logic = BinaryTreeLogic()
        nodes = logic.getTreeOf(state.actual_user.active_position, self.conf_binary_matrix_display_depth)

        return nodes

    def createNewUser(self, sponsor):
        users = User.objects.all()
        new_index = len(users)
        name = "user%d" % new_index
        newUser = User.objects.create(username=name, sponsor=sponsor)
        return newUser

    def createNewPosition(self, user, paid=True):
        pm = PositionManager()

        if user.isMaster():
            newPosition, isMatrixFull = pm.createNewPositionForMaster(user)
        else:
            newPosition, isMatrixFull = pm.createNewPosition(user.sponsor.active_position, user)

        user.active_position = newPosition
        user.save()

        if paid:
            self.payFee(user)

        if isMatrixFull:
            newPosition = self._handleFullMatrix(newPosition)

        return newPosition

    def _handleFullMatrix(self, position):
        # Get the root of the full matrix
        logic = BinaryTreeLogic()
        top = logic.getMatrixTop(position)
        # Pay commission to it, except for the master.
        if not top.user.isMaster():
            self.payCommission(top.user)
        # Place the root again, to its sponsor's matrix.
        top.user.save()
        return self.createNewPosition(top.user, False)

    def setActualUser(self, user):
        state = self._getState()
        state.actual_user = user
        state.save()

    def payCommission(self, user):
        user.money += self.commission
        user.save()
        master = self.getMaster()
        master.money -= self.commission
        master.save()

    def getMaster(self):
        return User.objects.get(id=1)

    def payFee(self, user):
        # User buys the product, money decrerases
        user.money -= self.price
        # It if bought from Master, so money increases
        master = self.getMaster()
        master.money += self.price
        master.save()
        user.save()

    def userLeaves(self, user):
        if user.isMaster():
            raise Controller.MasterCannotLeave
        for u in User.objects.filter(sponsor=user):
            u.sponsor = self.getMaster()
            u.save()

        user.leave()
