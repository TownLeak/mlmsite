#!/usr/bin/python
# -*- coding: utf-8
from collections import deque
import unicodedata


class BinaryTree:
    _levelsOfFullMatrix = 3

    class NodeIsEmpty:
        pass

    class NodeIsNotEmpty:
        pass

    class QueueIsEmpty:
        pass

    class LogicError:
        pass

    def _sumOfSquares(self, n):
        sum = 0

        for i in range(n):
            sum += 2 ** i

        return sum

    def _getNumberOfNodesToReturn(self, depth=_levelsOfFullMatrix):
        return self._sumOfSquares(depth)

    def placeNode(self, root, newNode):
        """Place a new node in the tree. A new node is a new product that is not yet in the tree.
           The root is a product node that is the parent of the actual (sub) tree - it is a sponsor product.
           This is a recursive function, where the root is always a new sub tree during the tree
           traversal. It will then fill the tree left-to-right, level-by-level."""
        # If root is empty, yield error
        if not root:
            raise BinaryTree.NodeIsEmpty

        if not newNode:
            raise BinaryTree.NodeIsEmpty
        # Initialize the placement activity: create an empty queue, add the root to it,
        # then invoke the placement logic. Placement logic works with the queue.
        queue = deque([root])
        (node, side) = self._placeNodeRecursiveLogic(queue)
        self._commitNewNode(node, side, newNode)

    def isMatrixFull(self, node):
        for i in range(self._levelsOfFullMatrix):
            if not node:
                return False

            node = node.right

        return True

    def getMatrixTop(self, node):
        """Determine who gets the commission if with the placement of node, a matrix gets full."""
        if not node:
            raise BinaryTree.NodeIsEmpty
        for i in range(self._levelsOfFullMatrix - 1):
            # If actual node has no parent, it means that we reached the parent of the tree (master).
            # In this case, master is the owner.
            if not node.parent:
                return None
            node = node.parent

        return node

    def _commitNewNode(self, node, side, newNode):
        """Saves a new child of a node (commits to the database)"""
        if not node or not side:
            raise BinaryTree.LogicError

        if not newNode:
            raise BinaryTree.NodeIsEmpty

        if side == "left":
            node.left = newNode
        elif side == "right":
            node.right = newNode
        else:
            raise BinaryTree.LogicError

        newNode.parent = node
        node.save()
        newNode.save()

    def _placeNodeRecursiveLogic(self, queue):
        # If queue empty, yield error. If newNode is none, yield error.
        if not queue:
            raise BinaryTree.QueueIsEmpty
        # Pop from the queue. If it is empty, yield error (the algorithm cannot place empty
        # node to the queue, beacuse the first empty node found is the placement node)
        actualNode = queue.popleft()
        if not actualNode:
            raise BinaryTree.NodeIsEmpty
        # If left node is full: put it go to the queue, take right node
        # else set good node to left node
        if actualNode.left:
            queue.append(actualNode.left)
            # if right node is full, put it to the queue, restart with the left node as root
            if actualNode.right:
                queue.append(actualNode.right)
                (actualNode, side) = self._placeNodeRecursiveLogic(queue)
            # else set good node to right node
            else:
                side = "right"
        else:
            side = "left"
        # Here, good node contains an empty node for placement.
        # Ensure that it is really empty.
        if not side:
            raise BinaryTree.NodeIsNotEmpty
        # Return the good node for placement
        return (actualNode, side)

    def _treeToJsonRecursive(self, root):
        children = []
        if root.left:
            children.append(self.treeToJson(root.left))
        if root.right:
            children.append(self.treeToJson(root.right))

        name = (u'%s (%s)') % (root.owner.username, root.owner.sponsor.username if root.owner.sponsor else "None")
        name = unicodedata.normalize("NFKD", name).encode('ascii', 'ignore')

        return {
            'id': ('%d' % root.id),
            'name': name,
            'data': {},
            'children': children
        }

    def treeToJson(self, root):
        return self._treeToJsonRecursive(root)
