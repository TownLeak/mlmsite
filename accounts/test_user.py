from django.utils import unittest
from django.contrib.auth.models import User
from userena.tests.profiles.test import ProfileTestCase


class TestUser(ProfileTestCase):
    f_username = 'testuser1'

    # -------------------------------------------------------------------------
    def setUp(self):
        self.f_u1 = User.objects.create(username=self.f_username)

    # -------------------------------------------------------------------------
    def tearDown(self):
        self.f_u1.delete()

    # -------------------------------------------------------------------------
    def test(self):
        self.assertEqual(self.f_u1.username, self.f_username)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(TestUser)
