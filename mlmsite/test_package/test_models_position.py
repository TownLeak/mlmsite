import unittest
from django.test import TestCase
from mlmsite.models import Position, User


class Tests(TestCase):
    def testCreateInDatabase(self):
        owner = User.objects.create(username="user")
        position = Position.CreateInDatabase(owner)
        self.assertEqual(owner.id, position.owner.id)
        self.assertFalse(position.closed)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
