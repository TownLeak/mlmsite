#!/usr/bin/python
# -*- coding: utf-8
from collections import deque


class BinaryTreeLogic:
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

    def _getTreeOfRecursiveLogic(self, queue, listOfNodes, numToReturn):
        # If the queue empty or the number of elements to retrieve is zero, terminate the logic
        if not numToReturn:
            return listOfNodes
        # Get the actual root
        if queue:
            root = queue.popleft()
        else:
            root = None

        if root:
            queue.append(root.left_guy)
            queue.append(root.right_guy)
        else:
            queue.append(None)
            queue.append(None)

        # Add the root (popped element) to the list
        listOfNodes.append(root)
        # Call recursively the logic with the new values
        return self._getTreeOfRecursiveLogic(queue, listOfNodes, numToReturn - 1)

    def getTreeOf(self, root, depth):
        # root cannot be invalid
        if not root:
            raise BinaryTreeLogic.NodeIsEmpty
        # Root is the first list element. Initialize the retrieval logic with it:
        # Create empty queue, add the root
        queue = deque([root])
        # Calculate the number of retrieved nodes by the depth variable
        numToReturn = self._getNumberOfNodesToReturn(depth)
        # start the recursive retrieval logic.
        return self._getTreeOfRecursiveLogic(queue, [], numToReturn)

    def placeNode(self, root, newNode):
        """Place a new node in the tree. A new node is a new product that is not yet in the tree.
           The root is a product node that is the top of the actual (sub) tree - it is a sponsor product.
           This is a recursive function, where the root is always a new sub tree during the tree
           traversal. It will then fill the tree left-to-right, level-by-level."""
        # If root is empty, yield error
        if not root:
            raise BinaryTreeLogic.NodeIsEmpty

        if not newNode:
            raise BinaryTreeLogic.NodeIsEmpty
        # Initialize the placement activity: create an empty queue, add the root to it,
        # then invoke the placement logic. Placement logic works with the queue.
        queue = deque([root])
        (node, side) = self._placeNodeRecursiveLogic(queue)
        self._commitNewNode(node, side, newNode)

    def isMatrixFull(self, node):
        for i in range(self._levelsOfFullMatrix):
            if not node:
                return False

            node = node.right_guy

        return True

    def getMatrixTop(self, node):
        """Determine who gets the commission if with the placement of node, a matrix gets full."""
        if not node:
            raise BinaryTreeLogic.NodeIsEmpty
        for i in range(self._levelsOfFullMatrix - 1):
            # If actual node has no sponsor, it means that we reached the top of the tree (master).
            # In this case, master is the owner.
            if not node.sponsor:
                return None
            node = node.sponsor

        return node

    def _commitNewNode(self, node, side, newNode):
        """Saves a new child of a node (commits to the database)"""
        if not node or not side:
            raise BinaryTreeLogic.LogicError

        if not newNode:
            raise BinaryTreeLogic.NodeIsEmpty

        if side == "left":
            node.left_guy = newNode
        elif side == "right":
            node.right_guy = newNode
        else:
            raise BinaryTreeLogic.LogicError

        newNode.sponsor = node
        node.save()
        newNode.save()

    def _placeNodeRecursiveLogic(self, queue):
        # If queue empty, yield error. If newNode is none, yield error.
        if not queue:
            raise BinaryTreeLogic.QueueIsEmpty
        # Pop from the queue. If it is empty, yield error (the algorithm cannot place empty
        # node to the queue, beacuse the first empty node found is the placement node)
        actualNode = queue.popleft()
        if not actualNode:
            raise BinaryTreeLogic.NodeIsEmpty
        # If left node is full: put it go to the queue, take right node
        # else set good node to left node
        if actualNode.left_guy:
            queue.append(actualNode.left_guy)
            # if right node is full, put it to the queue, restart with the left node as root
            if actualNode.right_guy:
                queue.append(actualNode.right_guy)
                (actualNode, side) = self._placeNodeRecursiveLogic(queue)
            # else set good node to right node
            else:
                side = "right"
        else:
            side = "left"
        # Here, good node contains an empty node for placement.
        # Ensure that it is really empty.
        if not side:
            raise BinaryTreeLogic.NodeIsNotEmpty
        # Return the good node for placement
        return (actualNode, side)
