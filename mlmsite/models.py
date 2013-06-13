#from neo4django.db import models
from django.db import models
from binary_tree_logic import BinaryTreeLogic


class Position(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey('User')
    left = models.ForeignKey('Position', null=True, related_name='position_left')
    right = models.ForeignKey('Position', null=True, related_name="position_right")
    top = models.ForeignKey('Position', null=True, related_name='position_top')
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    @classmethod
    def CreateInDatabase(cls, owner):
        name = "position%d" % len(cls.objects.all())
        return cls.objects.create(name=name, owner=owner)

    def placePosition(self, rootPosition):
        logic = BinaryTreeLogic()
        logic.placeNode(rootPosition, self)
        return logic.isMatrixFull(logic.getMatrixTop(self))


class User(models.Model):
    conf_username = "A Mester"
    username = models.CharField(max_length=64, unique=True)
    sponsor = models.ForeignKey('User', null=True, related_name='user_sponsor')
    active_position = models.ForeignKey(Position, null=True, related_name='user_position')
    money = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)

    class MasterCannotLeave(Exception):
        pass

    class SponsorMustBeDefined(Exception):
        pass

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.__str__()

    def leave(self):
        if self.isMaster():
            raise User.MasterCannotLeave

        self.isActive = False
        self.save()

    def addNewActivePosition(self):
        self.active_position = Position.CreateInDatabase(owner=self)
        isMatrixFull = self.active_position.placePosition(self.sponsor.active_position) if not self.isMaster() else False
        self.save()
        return isMatrixFull

    def isMaster(self):
        return self.username == User.conf_username

    @classmethod
    def CreateNewUser(cls, sponsor):
        if not sponsor:
            raise User.SponsorMustBeDefined
        return User.objects.create(username="user%d" % len(User.objects.all()), sponsor=sponsor)


class MasterUser(User):
    @classmethod
    def Get(cls):
        try:
            master = User.objects.get(username=MasterUser.conf_username)
        except User.DoesNotExist:
            master = User.objects.create(username=MasterUser.conf_username)
            master.active_position = Position.CreateInDatabase(owner=master)
            master.sponsor = master
            master.save()
        return master


class State(models.Model):
    actual_user = models.ForeignKey(User)
