#from neo4django.db import models
from django.db import models


# class Distributor(models.NodeModel):
#     """
#     Class represents a distributor. A distributor is in fact an MLM position.
#     An user may participate in several matrixes. Distributors are the nodes
#     of matrixes. When an user opens a position (starts building a matrix), he creates
#     a new distributor. A distributor may belong to one user only, ine user
#     may have several Distributors associated.
#     """

#     # User ID in the normal database.
#     userid = models.IntegerProperty()

#     sponsor = models.Relationship('Distributor',
#                                   rel_type='sponsors',
#                                   single=True,
#                                   related_name='sponsored_by')


# -----------------
# Models for graph eval
# -----------------
class GraphEval_User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    sponsor = models.ForeignKey('GraphEval_User', null=True, related_name='user_sponsor')
    active_position = models.ForeignKey('GraphEval_Position', null=True, related_name='user_position')
    money = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.__str__()

    def isMaster(self):
        return self.id == 1

    def leave(self):
        self.isActive = False
        self.save()


class GraphEval_Position(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(GraphEval_User)
    left_guy = models.ForeignKey('GraphEval_Position', null=True, related_name='position_left_guy')
    right_guy = models.ForeignKey('GraphEval_Position', null=True, related_name="position_right_guy")
    sponsor = models.ForeignKey('GraphEval_Position', null=True, related_name='position_sponsor')
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name


class GraphEval_State(models.Model):
    actual_user = models.ForeignKey(GraphEval_User)
