import unittest
from neo4django.testcases import NodeModelTestCase
from neo4django.db import models

# The tutorial: https://neo4django.readthedocs.org/en/latest/writing-models.html


class Person(models.NodeModel):
    "Model from the tutorial."
    name = models.StringProperty()
    age = models.IntegerProperty()

    friends = models.Relationship('self', rel_type='friends_with')


class OnlinePerson(Person):
    email = models.EmailProperty()
    homepage = models.URLProperty()


class EmployedPerson(Person):
    job_title = models.StringProperty(indexed=True)


class Pet(models.NodeModel):
    owner = models.Relationship(Person,
                                rel_type='owns',
                                single=True,
                                related_name='pets')


class Tests(NodeModelTestCase):
    """Tests from the neo4django tutorial. Purpose: learn neo4django, and use these tests to verify concepts."""

    def test(self):
        pete = Person.objects.create(name='Pete', age=30)
        self.assertEqual(pete.name, 'Pete')
        self.assertEqual(pete.age, 30)
        garfield = Pet.objects.create()
        pete.pets.add(garfield)
        pete.save()
        pete_pets = list(pete.pets.all())
        self.assertEqual(len(pete_pets), 1)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
