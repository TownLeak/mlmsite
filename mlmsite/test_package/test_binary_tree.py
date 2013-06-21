import unittest
from django.test import TestCase
from mlmsite.binary_tree import BinaryTree
from collections import deque
from mlmsite.models import BinaryPosition
from mlmsite.models import User


class DummyUser:
    def __init__(self, username, sponsor=None):
        self.username = username
        self.sponsor = sponsor


class DummyNode:
    def __init__(self, id, parent=None, owner=None):
        self.saved = False
        self.id = id
        self.right = None
        self.left = None
        self.parent = parent
        self.isCommissionPaid = False
        self.owner = owner

    def __str__(self):
        return str(self.id)

    def save(self):
        self.saved = True

    def payCommission(self):
        self.isCommissionPaid = True


class Tests(TestCase):
    def setUp(self):
        self.root = DummyNode(1)
        self.logic = BinaryTree()

    def testPlaceNodeCatchEmptyNodes(self):
        notEmptyNode = 1

        with self.assertRaises(BinaryTree.NodeIsEmpty):
            self.logic.placeNode(None, notEmptyNode)

        with self.assertRaises(BinaryTree.NodeIsEmpty):
            self.logic.placeNode(notEmptyNode, None)

    def testPlaceNodeRecursiveLogicCatchEmpties(self):
        with self.assertRaises(BinaryTree.QueueIsEmpty):
            queue = deque([])
            self.logic._placeNodeRecursiveLogic(queue)

        with self.assertRaises(BinaryTree.NodeIsEmpty):
            queue = deque([None])
            self.logic._placeNodeRecursiveLogic(queue)

    def testPlaceNodeRecursiveLogicTestLeftPlacement(self):
        queue = deque([self.root])
        (actualNode, side) = self.logic._placeNodeRecursiveLogic(queue)
        self.assertEqual(side, "left")
        self.assertEqual(actualNode, self.root)

    def testPlaceNodeRecursiveLogicTestRightPlacement(self):
        self.root.left = DummyNode(2)
        queue = deque([self.root])
        (actualNode, side) = self.logic._placeNodeRecursiveLogic(queue)
        self.assertEqual(side, "right")
        self.assertEqual(actualNode, self.root)

    def testPlaceNodeRecursiveLogicTestOneLevelDown(self):
        self.root.left = DummyNode(2)
        self.root.right = DummyNode(3)
        self.root.left.left = DummyNode(4)
        queue = deque([self.root])
        (actualNode, side) = self.logic._placeNodeRecursiveLogic(queue)
        self.assertEqual(side, "right")
        self.assertEqual(actualNode, self.root.left)

    def testPlaceNodeRecursiveLogicTestOneLevelDownThreeNodesRight(self):
        self.root.left = DummyNode(2)
        self.root.right = DummyNode(3)
        self.root.left.left = DummyNode(4)
        self.root.left.right = DummyNode(5)
        queue = deque([self.root])
        (actualNode, side) = self.logic._placeNodeRecursiveLogic(queue)
        self.assertEqual(side, "left")
        self.assertEqual(actualNode, self.root.right)

    def testPlaceNodeSaves(self):
        newNode = DummyNode(2)
        self.assertFalse(self.root.saved)
        self.assertEqual(self.root.left, None)
        self.logic.placeNode(self.root, newNode)
        self.assertEqual(self.root.left, newNode)
        self.assertTrue(self.root.saved)

    def testCommitNewNode(self):
        node = DummyNode(1)
        newNode = DummyNode(2)
        newNode.sponsor = node

        with self.assertRaises(BinaryTree.LogicError):
            self.logic._commitNewNode(None, "left", node)

        with self.assertRaises(BinaryTree.LogicError):
            self.logic._commitNewNode(node, "", node)

        with self.assertRaises(BinaryTree.NodeIsEmpty):
            self.logic._commitNewNode(node, "left", None)

        with self.assertRaises(BinaryTree.LogicError):
            self.logic._commitNewNode(node, "atyala", node)

        self.logic._commitNewNode(node, "left", newNode)
        self.assertTrue(node.left)
        self.assertEqual(node.left.id, 2)
        self.assertFalse(node.right)
        self.assertEqual(newNode.sponsor, node)

        node = DummyNode(1)
        newNode.sponsor = node
        self.logic._commitNewNode(node, "right", newNode)
        self.assertTrue(node.right)
        self.assertEqual(node.right.id, 2)
        self.assertFalse(node.left)
        self.assertEqual(newNode.sponsor, node)

    def _testPersistencyCreate(self):
        user = User.objects.create(username="user1")
        self.root = BinaryPosition.objects.create(name="pos1", owner=user)
        newNode = BinaryPosition.objects.create(name="pos2", owner=user)
        self.assertEqual(self.root.left, None)
        self.logic.placeNode(self.root, newNode)
        self.assertEqual(self.root.left, newNode)

    def testPersistency(self):
        self._testPersistencyCreate()
        self.root = BinaryPosition.objects.get(name="pos1")
        newNode = BinaryPosition.objects.get(name="pos2")
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


    def testIsMatrixFull(self):
        self.logic._levelsOfFullMatrix = 2
        node = DummyNode(1)
        self.assertFalse(self.logic.isMatrixFull(node))
        node.left = DummyNode(2)
        self.assertFalse(self.logic.isMatrixFull(node))
        node.right = DummyNode(3)
        self.assertTrue(self.logic.isMatrixFull(node))

    def _testHandleFullMatrixOnePlacement(self):
        self.logic._levelsOfFullMatrix = 2

        with self.assertRaises(BinaryTree.NodeIsEmpty):
            self.logic._handleFullMatrix(None)
        # Set up test
        self.logic.placeNode(self.root, DummyNode(2))
        self.logic.placeNode(self.root, DummyNode(3))
        self.logic.placeNode(self.root.left, DummyNode(4))
        self.logic.placeNode(self.root.left, DummyNode(5))
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
        self.root.left = DummyNode(2)
        queue = deque([self.root])
        (node, side, isMatrixFull) = self.logic._placeNodeRecursiveLogic(queue, 1)
        self.assertEqual(node, self.root)
        self.assertEqual(side, "right")
        self.assertTrue(isMatrixFull)

    def testGetMatrixTop(self):
        self.logic._levelsOfFullMatrix = 2
        self.logic.placeNode(self.root, DummyNode(2))
        self.logic.placeNode(self.root.left, DummyNode(3))
        self.assertEqual(self.root, self.logic.getMatrixTop(self.root.left))
        self.logic._levelsOfFullMatrix = 3
        self.logic.placeNode(self.root, DummyNode(4))
        self.logic.placeNode(self.root.right, DummyNode(5))
        self.assertEqual(self.root, self.logic.getMatrixTop(self.root.right.left))
        # Test if we are too close to the parent: we cannot go beyont teh parentmost node (master),
        # in this case, the method must return None.
        self.assertEqual(None, self.logic.getMatrixTop(self.root.right))

    def testTreeToJson_OneNode(self):
        node = DummyNode(1, owner=DummyUser("user1"))
        json = self.logic.treeToJson(node)
        self.assertEqual("{'children': [], 'data': {}, 'id': '1', 'name': 'user1 (None)'}", str(json))

    def testTreeToJson_TwoNodes(self):
        user1 = DummyUser("user1")
        node1 = DummyNode(1, owner=user1)
        node2 = DummyNode(2, parent=node1, owner=DummyUser("user2", user1))
        node1.left = node2
        json = self.logic.treeToJson(node1)
        self.assertEqual("{'children': [{'children': [], 'data': {}, 'id': '2', 'name': 'user2 (user1)'}], 'data': {}, 'id': '1', 'name': 'user1 (None)'}", str(json))


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
