#!/usr/bin/python
# -*- coding: utf-8
from models import User, State, MasterUser
from binary_tree import BinaryTree
from django.utils.translation import ugettext as _
from unilevel_tree import UnilevelTree
from collections import deque


class Controller:
    class UnknownTreeView(Exception):
        pass

    price = 1000
    monthly_fee = 100
    commission = 2 * price
    monthly_percent = 10
    conf_binary_matrix_display_depth = 3
    conf_unilevel_copmmission_depth = 5

    def __init__(self):
        if not State.objects.all():
            State.objects.create(actual_user=MasterUser.Get())

    def _getState(self):
        return State.objects.get(id=1)

    def getActualUser(self):
        return self._getState().actual_user

    def getActualData(self):
        state = self._getState()
        logic = BinaryTree()
        return logic.getTreeOf(state.actual_user.active_binary_position, self.conf_binary_matrix_display_depth)

    def createNewBinaryPosition(self, userId, toPayPrice=True):
        isMatrixFull = User.Get(userId).addNewActiveBinaryPosition()

        if toPayPrice:
            self.payBinaryPrice(userId)

        return self._handleFullMatrix(User.Get(userId).active_binary_position) if isMatrixFull else User.Get(userId).active_binary_position

    def createNewUnilevelPosition(self, userId):
        User.Get(userId).addNewActiveUnilevelPosition()

    def _handleFullMatrix(self, position):
        # Get the root of the full matrix
        top = BinaryTree().getMatrixTop(position)
        # Pay commission to it, except for the master.
        if not top.owner.isMaster():
            self.payBinaryCommission(top.owner.id)
        # Place the root again, to its sponsor's matrix.
        return self.createNewBinaryPosition(top.owner.id, toPayPrice=False)

    def setActualUser(self, user):
        state = self._getState()
        state.actual_user = user
        state.save()

    def payBinaryCommission(self, userId):
        user = User.Get(userId)
        user.binary_money += self.commission
        user.save()
        master = MasterUser.Get()
        master.binary_money -= self.commission
        master.save()

    def payBinaryPrice(self, userId):
        user = User.Get(userId)
        # User buys the product, money decrerases
        user.binary_money -= self.price
        # It if bought from Master, so money increases
        master = MasterUser.Get()
        master.binary_money += self.price
        master.save()
        user.save()

    def userLeaves(self, userId):
        user = User.Get(userId)
        user.leave()

        for u in User.objects.filter(sponsor=user):
            u.sponsor = MasterUser.Get()
            u.save()

    def getActualTree(self):
        state = self._getState()
        if state.tree_view == State.BINARY_TREE:
            logic = BinaryTree()
            return logic.treeToJson(state.actual_user.active_binary_position)
        elif state.tree_view == State.UNILEVEL_TREE:
            logic = UnilevelTree()
            return logic.treeToJson(state.actual_user.active_unilevel_position)
        else:
            raise Controller.UnknownTreeView

    def _switchToMatrix(self, matrix):
        state = self._getState()
        state.tree_view = matrix
        state.save()

    def switchToBinaryMatrix(self):
        self._switchToMatrix(State.BINARY_TREE)

    def switchToUnilevelMatrix(self):
        self._switchToMatrix(State.UNILEVEL_TREE)

    def getActualTreeName(self):
        return _(u"Binary matrix") if self._getState().tree_view == State.BINARY_TREE else "Unilevel matrix"

    def advanceToNextMonth(self):
        state = self._getState()
        state.month += 1
        state.save()
        self.executeMonthlyPayments()

    def getActualMonth(self):
        return self._getState().month

    def createNewUser(self, sponsor):
        userId = User.CreateNewUser(sponsor=sponsor).id
        self.createNewBinaryPosition(userId)
        self.createNewUnilevelPosition(userId)
        return userId

    def calculateMonthlyCommission(self):
        return self.monthly_fee * self.monthly_percent / 100

    def payMonthlyCommission(self, userId):
        user = User.Get(userId)
        commission = self.calculateMonthlyCommission() * user.active_unilevel_position.countChildren(self.conf_unilevel_copmmission_depth)
        user.unilevel_money += commission
        user.save()
        return commission

    def executeMonthlyPayments(self):
        master = MasterUser.Get()

        for user in User.objects.all():
            if not user.isMaster():
                user.unilevel_money -= self.monthly_fee
                user.save()
                master.unilevel_money += (self.monthly_fee - self.payMonthlyCommission(user.id))

        master.save()

    def _createMoreNewUsersRecursive(self, queue, callNum, limit):
        sponsor = User.Get(queue.popleft())
        for i in range(2):
            queue.append(self.createNewUser(sponsor=sponsor))
            if (callNum + i + 1) == limit:
                return

        self._createMoreNewUsersRecursive(queue, callNum + 2, limit)

    def createMoreNewUsers(self, limit):
        self._createMoreNewUsersRecursive(deque([MasterUser.Get().id]), 0, limit)
