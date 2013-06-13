import unittest
from django.test import TestCase
from mlmsite.binary_tree_logic import BinaryTreeLogic
from collections import deque
from mlmsite.models import Position, User


class Tests(TestCase):
    def _createTestPosition(self, owner=None):
        realOwner = User.objects.create(username="User %d" % len(User.objects.all())) if not owner else owner
        return Position.CreateInDatabase(owner=realOwner)

    def setUp(self):
        self.root = self._createTestPosition()
        self.logic = BinaryTreeLogic()

    def testPlaceNodeCatchEmptyNodes(self):
        notEmptyNode = 1

        with self.assertRaises(BinaryTreeLogic.NodeIsEmpty):
            self.logic.placeNode(None, notEmptyNode)

        with self.assertRaises(BinaryTreeLogic.NodeIsEmpty):
            self.logic.placeNode(notEmptyNode, None)

    def testPlaceNodeRecursiveLogicCatchEmpties(self):
        with self.assertRaises(BinaryTreeLogic.QueueIsEmpty):
            queue = deque([])
            self.logic._placeNodeRecursiveLogic(queue)

        with self.assertRaises(BinaryTreeLogic.NodeIsEmpty):
            queue = deque([None])
            self.logic._placeNodeRecursiveLogic(queue)

    def testPlaceNodeRecursiveLogicTestLeftPlacement(self):
        queue = deque([self.root])
        (actualNode, side) = self.logic._placeNodeRecursiveLogic(queue)
        self.assertEqual(side, "left")
        self.assertEqual(actualNode, self.root)

    def testPlaceNodeRecursiveLogicTestRightPlacement(self):
        self.root.left = self._createTestPosition()
        queue = deque([self.root])
        (actualNode, side) = self.logic._placeNodeRecursiveLogic(queue)
        self.assertEqual(side, "right")
        self.assertEqual(actualNode, self.root)

    def testPlaceNodeRecursiveLogicTestOneLevelDown(self):
        self.root.left = self._createTestPosition()
        self.root.right = self._createTestPosition()
        self.root.left.left = self._createTestPosition()
        queue = deque([self.root])
        (actualNode, side) = self.logic._placeNodeRecursiveLogic(queue)
        self.assertEqual(side, "right")
        self.assertEqual(actualNode, self.root.left)

    def testPlaceNodeRecursiveLogicTestOneLevelDownThreeNodesRight(self):
        self.root.left = self._createTestPosition()
        self.root.right = self._createTestPosition()
        self.root.left.left = self._createTestPosition()
        self.root.left.right = self._createTestPosition()
        queue = deque([self.root])
        (actualNode, side) = self.logic._placeNodeRecursiveLogic(queue)
        self.assertEqual(side, "left")
        self.assertEqual(actualNode, self.root.right)

    def testCommitNewNode(self):
        node = self._createTestPosition()
        newNode = self._createTestPosition()
        newNode.sponsor = node

        with self.assertRaises(BinaryTreeLogic.LogicError):
            self.logic._commitNewNode(None, "left", node)

        with self.assertRaises(BinaryTreeLogic.LogicError):
            self.logic._commitNewNode(node, "", node)

        with self.assertRaises(BinaryTreeLogic.NodeIsEmpty):
            self.logic._commitNewNode(node, "left", None)

        with self.assertRaises(BinaryTreeLogic.LogicError):
            self.logic._commitNewNode(node, "atyala", node)

        self.logic._commitNewNode(node, "left", newNode)
        self.assertTrue(node.left)
        self.assertEqual(node.left.id, newNode.id)
        self.assertFalse(node.right)
        self.assertEqual(newNode.sponsor, node)

        node = self._createTestPosition()
        newNode.sponsor = node
        self.logic._commitNewNode(node, "right", newNode)
        self.assertTrue(node.right)
        self.assertEqual(node.right.id, newNode.id)
        self.assertFalse(node.left)
        self.assertEqual(newNode.sponsor, node)

    def _testPersistencyCreate(self):
        user = User.objects.create(username="user1")
        self.root = Position.objects.create(name="pos1", owner=user)
        newNode = Position.objects.create(name="pos2", owner=user)
        self.assertEqual(self.root.left, None)
        self.logic.placeNode(self.root, newNode)
        self.assertEqual(self.root.left, newNode)

    def testPersistency(self):
        self._testPersistencyCreate()
        self.root = Position.objects.get(name="pos1")
        newNode = Position.objects.get(name="pos2")
        self.assertTrue(self.root)
        self.assertTrue(newNode)
        self.assertEqual(self.root.left, newNode)

    def testGetNumberOfNodesToReturn(self):
        self.assertEqual(1, self.logic._getNumberOfNodesToReturn(1))
        self.assertEqual(3, self.logic._getNumberOfNodesToReturn(2))
        self.assertEqual(7, self.logic._getNumberOfNodesToReturn(3))

    def testSumOfSquares(self):
        self.assertEqual(1, self.logic._sumOfSquares(1))
        self.assertEqual(3, self.logic._sumOfSquares(2))
        self.assertEqual(7, self.logic._sumOfSquares(3))

    def testGetTreeOfRecursiveLogicDepth0(self):
        queue = deque([])
        listOfNodes = self.logic._getTreeOfRecursiveLogic(queue, [], 2)
        self.assertEqual(listOfNodes, [None, None])

        queue = deque([None])
        listOfNodes = self.logic._getTreeOfRecursiveLogic(queue, [], 2)
        self.assertEqual(listOfNodes, [None, None])

        listOfNodes = self.logic._getTreeOfRecursiveLogic(queue, [], 0)
        self.assertFalse(listOfNodes)

    def testGetTreeOfRecursiveLogicDepth1(self):
        node = self._createTestPosition()
        queue = deque([node])
        listOfNodes = []
        self.logic._getTreeOfRecursiveLogic(queue, listOfNodes, 1)
        self.assertEqual(len(listOfNodes), 1)
        self.assertEqual(listOfNodes[0], node)

    def testGetTreeOfRecursiveLogicDepth2Full(self):
        node = self._createTestPosition()
        node.left = self._createTestPosition()
        node.right = self._createTestPosition()
        queue = deque([node])
        listOfNodes = []
        # 3: number of returned elements at level 2 (1 + 2...)
        self.logic._getTreeOfRecursiveLogic(queue, listOfNodes, 3)
        self.assertEqual(len(listOfNodes), 3)
        self.assertEqual(listOfNodes[0], node)
        self.assertEqual(listOfNodes[1], node.left)
        self.assertEqual(listOfNodes[2], node.right)

    def testGetTreeOfRecursiveLogicDepth3PartialOnLeft(self):
        node = self._createTestPosition()
        node.left = self._createTestPosition()
        node.right = self._createTestPosition()
        node.left.left = self._createTestPosition()
        queue = deque([node])
        listOfNodes = []
        # 7: number of returned elements at level 3 (1 + 2 + 4...)
        self.logic._getTreeOfRecursiveLogic(queue, listOfNodes, 7)
        self.assertEqual(len(listOfNodes), 7)
        self.assertEqual(listOfNodes[0], node)
        self.assertEqual(listOfNodes[1], node.left)
        self.assertEqual(listOfNodes[2], node.right)
        self.assertEqual(listOfNodes[3], node.left.left)
        self.assertFalse(listOfNodes[4])
        self.assertFalse(listOfNodes[5])
        self.assertFalse(listOfNodes[6])

    def testGetTreeOfRecursiveLogicDepth3PartialOnRight(self):
        node = self._createTestPosition()
        node.left = self._createTestPosition()
        node.right = self._createTestPosition()
        node.right.left = self._createTestPosition()
        queue = deque([node])
        listOfNodes = []
        # 7: number of returned elements at level 3 (1 + 2 + 4...)
        self.logic._getTreeOfRecursiveLogic(queue, listOfNodes, 7)
        self.assertEqual(len(listOfNodes), 7)
        self.assertEqual(listOfNodes[0], node)
        self.assertEqual(listOfNodes[1], node.left)
        self.assertEqual(listOfNodes[2], node.right)
        self.assertFalse(listOfNodes[3])
        self.assertFalse(listOfNodes[4])
        self.assertEqual(listOfNodes[5], node.right.left)
        self.assertFalse(listOfNodes[6])

    def testGetTreeOfNullRoot(self):
        with self.assertRaises(BinaryTreeLogic.NodeIsEmpty):
            self.logic.getTreeOf(None, 2)

        listOfNodes = self.logic.getTreeOf(self._createTestPosition(), 0)
        self.assertFalse(listOfNodes)

    def testGetTreeOfDepth2(self):
        node = self._createTestPosition()
        node.left = self._createTestPosition()
        node.right = self._createTestPosition()
        listOfNodes = self.logic.getTreeOf(node, 2)
        self.assertEqual(len(listOfNodes), 3)
        self.assertEqual(listOfNodes[0], node)
        self.assertEqual(listOfNodes[1], node.left)
        self.assertEqual(listOfNodes[2], node.right)

    def testIsMatrixFull(self):
        self.logic._levelsOfFullMatrix = 2
        node = self._createTestPosition()
        self.assertFalse(self.logic.isMatrixFull(node))
        node.left = self._createTestPosition()
        self.assertFalse(self.logic.isMatrixFull(node))
        node.right = self._createTestPosition()
        self.assertTrue(self.logic.isMatrixFull(node))

    def _testHandleFullMatrixOnePlacement(self):
        self.logic._levelsOfFullMatrix = 2

        with self.assertRaises(BinaryTreeLogic.NodeIsEmpty):
            self.logic._handleFullMatrix(None)
        # Set up test
        self.logic.placeNode(self.root, self._createTestPosition())
        self.logic.placeNode(self.root, self._createTestPosition())
        self.logic.placeNode(self.root.left, self._createTestPosition())
        self.logic.placeNode(self.root.left, self._createTestPosition())
        self.assertFalse(self.root.isCommissionPaid)
        # Test body
        self.assertFalse(self.root.right.left)
        self.logic._handleFullMatrix(self.root.left.right)
        self.assertEqual(self.root.right.left, self.root.left.right)
        self.assertTrue(self.root.isCommissionPaid)

    def _testPlaceNodeFullMatrix(self):
        self.logic._levelsOfFullMatrix = 2
        # Test that in case of not full matrix, isMatrixFull is false
        queue = deque([self.root])
        (node, side, isMatrixFull) = self.logic._placeNodeRecursiveLogic(queue, 1)
        self.assertEqual(node, self.root)
        self.assertEqual(side, "left")
        self.assertFalse(isMatrixFull)
        # Test that in case of not full matrix, isMatrixFull is true
        self.root.left = self._createTestPosition()
        queue = deque([self.root])
        (node, side, isMatrixFull) = self.logic._placeNodeRecursiveLogic(queue, 1)
        self.assertEqual(node, self.root)
        self.assertEqual(side, "right")
        self.assertTrue(isMatrixFull)

    def testGetMatrixTop(self):
        self.logic._levelsOfFullMatrix = 2
        self.logic.placeNode(self.root, self._createTestPosition())
        self.logic.placeNode(self.root.left, self._createTestPosition())
        self.assertEqual(self.root, self.logic.getMatrixTop(self.root.left))
        self.logic._levelsOfFullMatrix = 3
        self.logic.placeNode(self.root, self._createTestPosition())
        self.logic.placeNode(self.root.right, self._createTestPosition())
        self.assertEqual(self.root, self.logic.getMatrixTop(self.root.right.left))
        # Test if we are too close to the top: we cannot go beyont teh topmost node (master),
        # in this case, the method must return None.
        self.assertEqual(None, self.logic.getMatrixTop(self.root.right))

    def testTreeToJson_OneNode(self):
        node = Position.CreateInDatabase(owner=User.objects.create(username="user1"))
        json = self.logic.treeToJson(node)
        self.assertEqual("{'children': [], 'data': {}, 'id': '%d', 'name': 'user1 (None)'}" % node.id, str(json))

    def testTreeToJson_TwoNodes(self):
        user1 = User.objects.create(username="user1")
        node1 = Position.CreateInDatabase(owner=user1)
        node2 = Position.objects.create(name="Name", top=node1, owner=User.objects.create(username="user2", sponsor=user1))
        node1.left = node2
        json = self.logic.treeToJson(node1)
        self.assertEqual("{'children': [{'children': [], 'data': {}, 'id': '%d', 'name': 'user2 (user1)'}], 'data': {}, 'id': '%d', 'name': 'user1 (None)'}" % (node2.id, node1.id), str(json))


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
