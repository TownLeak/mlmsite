#!/usr/bin/python
# -*- coding: utf-8
from models import User, Position, State, MasterUser
from binary_tree import BinaryTree
#from unilevel_tree import UnilevelTree


class Controller:
    class UnknownTreeView(Exception):
        pass

    price = 100
    commission = 2 * price
    user_type = User
    state_type = State
    position_type = Position
    conf_binary_matrix_display_depth = 3

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

    def createNewBinaryPosition(self, user, paid=True):
        isMatrixFull = user.addNewActiveBinaryPosition()

        if paid:
            self.payFee(user)

        return self._handleFullMatrix(user.active_binary_position) if isMatrixFull else user.active_binary_position

    def _handleFullMatrix(self, position):
        # Get the root of the full matrix
        logic = BinaryTree()
        top = logic.getMatrixTop(position)
        # Pay commission to it, except for the master.
        if not top.owner.isMaster():
            self.payCommission(top.owner)
        # Place the root again, to its sponsor's matrix.
        top.owner.save()
        return self.createNewBinaryPosition(top.owner, False)

    def setActualUser(self, user):
        state = self._getState()
        state.actual_user = user
        state.save()

    def payCommission(self, user):
        user.money += self.commission
        user.save()
        master = MasterUser.Get()
        master.money -= self.commission
        master.save()

    def payFee(self, user):
        # User buys the product, money decrerases
        user.money -= self.price
        # It if bought from Master, so money increases
        master = MasterUser.Get()
        master.money += self.price
        master.save()
        user.save()

    def userLeaves(self, user):
        user.leave()

        for u in User.objects.filter(sponsor=user):
            u.sponsor = MasterUser.Get()
            u.save()

    def getActualTree(self):
        state = self._getState()
        if state.tree_view == State.BINARY_TREE:
            logic = BinaryTree()
            return logic.treeToJson(state.actual_user.active_binary_position)
        #elif state.tree_view == State.UNILEVEL_TREE:
#            logic = UnilevelTree()
            #return logic.treeToJson(state.actual_user.active_unilevel_position)
        else:
            raise Controller.UnknownTreeView
