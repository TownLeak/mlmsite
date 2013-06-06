import unittest
from neo4django.testcases import NodeModelTestCase
from mlmsite.models import Distributor


class Tests(NodeModelTestCase):
    f_userid = 6

    def testProperties(self):
        dist = Distributor.objects.create(userid=6)
        self.assertEqual(dist.userid, self.f_userid)

    def testRelationship(self):
        joe = Distributor.objects.create(userid=6)
        dick = Distributor.objects.create(userid=7)
        ray = Distributor.objects.create(userid=8)
        
        joe.sponsored_by.add(dick)
        joe_sponsors = list(joe.sponsors.all())
        self.assertEqual(len(joe_sponsors), 1)
        
        joe.sponsored_by.add(ray)
        joe_sponsors = list(joe.sponsors.all())
        self.assertEqual(len(joe_sponsors), 2)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
