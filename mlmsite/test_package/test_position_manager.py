import unittest
from django.test import TestCase
from mlmsite.position_manager import PositionManager
from mlmsite.binary_tree_logic import BinaryTreeLogic


class User:
    pass


class Position:
    left_guy = None
    right_guy = None
    sponsor = None

    def save(self):
        pass

    class objects:
        @classmethod
        def all(cls):
            return []

        @classmethod
        def create(cls, name, user):
            return Position()


class Tests(TestCase):
    def setUp(self):
        self.pm = PositionManager()
        self.pm.position_type = Position

    def testCreateNewPosition(self):
        user = User()
        rootPosition = Position()
        newPosition, isFull = self.pm.createNewPosition(rootPosition, user)
        self.assertTrue(newPosition)
        self.assertEqual(rootPosition.left_guy, newPosition)

    def testCreateNewPositionDetectsFullMatrix(self):
        self.assertEqual(3, BinaryTreeLogic()._levelsOfFullMatrix, "The test assumes that the levels o fdill matrix is 3. Change test if it changes!")
        rootPosition = Position()
        newPosition, isFull = self.pm.createNewPosition(rootPosition, User())
        self.assertTrue(newPosition)
        self.assertEqual(newPosition.sponsor, rootPosition)
        newPosition, isFull = self.pm.createNewPosition(rootPosition, User())
        self.assertTrue(newPosition)
        self.assertEqual(newPosition.sponsor, rootPosition)
        newPosition, isFull = self.pm.createNewPosition(rootPosition, User())
        self.assertTrue(newPosition)
        self.assertEqual(newPosition.sponsor.sponsor, rootPosition)
        newPosition, isFull = self.pm.createNewPosition(rootPosition, User())
        self.assertTrue(newPosition)
        self.assertEqual(newPosition.sponsor.sponsor, rootPosition)
        newPosition, isFull = self.pm.createNewPosition(rootPosition, User())
        self.assertFalse(isFull)
        self.assertTrue(newPosition)
        self.assertEqual(newPosition.sponsor.sponsor, rootPosition)
        newPosition, isFull = self.pm.createNewPosition(rootPosition, User())
        self.assertTrue(isFull)
        self.assertTrue(newPosition)
        self.assertEqual(newPosition.sponsor.sponsor, rootPosition)
        newPosition, isFull = self.pm.createNewPosition(rootPosition, User())
        self.assertTrue(newPosition)
        self.assertEqual(newPosition.sponsor.sponsor.sponsor, rootPosition)
        self.assertFalse(isFull)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
