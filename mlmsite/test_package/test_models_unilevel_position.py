import unittest
from django.test import TestCase
from mlmsite.models import UnilevelPosition, User


class Tests(TestCase):
    def testCountChildren(self):
        # Test leaf node. Children count must ne 0.
        owner = User.objects.create(username="User")
        position_1 = UnilevelPosition.objects.create(owner=owner)
        self.assertEqual(0, position_1.countChildren(5))
        self.assertEqual(0, position_1.countChildren(0))
        # Test two nodes on level 1
        position_1_1 = UnilevelPosition.objects.create(owner=owner, parent=position_1)
        position_1_1.save()
        self.assertEqual(0, position_1.countChildren(0))
        self.assertEqual(1, position_1.countChildren(1))
        self.assertEqual(1, position_1.countChildren(5))
        position_1_2 = UnilevelPosition.objects.create(owner=owner, parent=position_1)
        position_1_2.save()
        self.assertEqual(2, position_1.countChildren(1))
        # Test the case when there are nodes below the required depth
        position_1_1_1 = UnilevelPosition.objects.create(owner=owner, parent=position_1_1)
        position_1_1_1.save()
        self.assertEqual(2, position_1.countChildren(1))
        self.assertEqual(1, position_1_1.countChildren(1))
        self.assertEqual(0, position_1_1_1.countChildren(1))


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
