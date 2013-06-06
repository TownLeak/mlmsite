#!/usr/bin/python
# -*- coding: utf-8
from models import GraphEval_Position as Position
from binary_tree_logic import BinaryTreeLogic


class PositionManager:
    position_type = Position

    def createNewPosition(self, rootPosition, user):
        positions = self.position_type.objects.all()
        new_index = len(positions)
        name = "position%d" % new_index
        newPosition = self.position_type.objects.create(name=name, user=user)
        logic = BinaryTreeLogic()
        logic.placeNode(rootPosition, newPosition)
        owner = logic.getMatrixTop(newPosition)
        isMatrixFull = logic.isMatrixFull(owner)
        return newPosition, isMatrixFull
