from django.db import models
from binary_tree import BinaryTree
from mptt.models import MPTTModel, TreeForeignKey


class Position(MPTTModel):
    class Meta:
        abstract = True

    name = models.CharField(max_length=256)
    owner = models.ForeignKey('User')
    closed = models.BooleanField(default=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name


class BinaryPosition(Position):
    left = models.ForeignKey('BinaryPosition', null=True, related_name='position_left')
    right = models.ForeignKey('BinaryPosition', null=True, related_name="position_right")

    def placePosition(self, rootPosition):
        logic = BinaryTree()
        logic.placeNode(rootPosition, self)
        return logic.isMatrixFull(logic.getMatrixTop(self))


class UnilevelPosition(Position):
    def countChildren(self, depth):
        level = self.get_level()
        count = 0
        for child in self.get_descendants():
            if child.get_level() - level <= depth:
                count += 1

        return count


class User(models.Model):
    conf_username = "A Mester"
    username = models.CharField(max_length=64, unique=True)
    sponsor = models.ForeignKey('User', null=True, related_name='user_sponsor')
    active_binary_position = models.ForeignKey(BinaryPosition, null=True, related_name='user_binary_position')
    active_unilevel_position = models.ForeignKey('UnilevelPosition', null=True, related_name='user_unilevel_position')
    binary_money = models.IntegerField(default=0)
    unilevel_money = models.IntegerField(default=0)
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

    def addNewActiveBinaryPosition(self):
        name = "binary_position%d" % len(BinaryPosition.objects.all())
        self.active_binary_position = BinaryPosition.objects.create(name=name, owner=self)
        isMatrixFull = self.active_binary_position.placePosition(self.sponsor.active_binary_position) if not self.isMaster() else False
        self.save()
        return isMatrixFull

    def addNewActiveUnilevelPosition(self):
        name = "unilevel_position%d" % len(UnilevelPosition.objects.all())
        self.active_unilevel_position = UnilevelPosition.objects.create(name=name, owner=self, parent=self.sponsor.active_unilevel_position if self.sponsor else None)
        self.save()

    def isMaster(self):
        return self.username == User.conf_username

    @classmethod
    def CreateNewUser(cls, sponsor):
        if not sponsor:
            raise User.SponsorMustBeDefined
        return User.objects.create(username="user%d" % len(User.objects.all()), sponsor=sponsor)

    @classmethod
    def IdOfFirstOrdinaryUser(cls):
        return 2

    @classmethod
    def Get(cls, id):
        return cls.objects.get(id=id)


class MasterUser(User):
    @classmethod
    def Get(cls):
        try:
            master = User.objects.get(username=MasterUser.conf_username)
        except User.DoesNotExist:
            master = User.objects.create(username=MasterUser.conf_username)
            master.addNewActiveBinaryPosition()
            master.addNewActiveUnilevelPosition()
            master.sponsor = master
            master.save()
        return master


class State(models.Model):
    actual_user = models.ForeignKey(User)
    month = models.IntegerField(default=0)

    BINARY_TREE = 'B'
    UNILEVEL_TREE = 'U'

    tree_view = models.CharField(max_length=1, choices=(
        (BINARY_TREE, "Binary"),
        (UNILEVEL_TREE, "Unilevel")),
        default=BINARY_TREE
    )

    def __str__(self):
        return "Actual user: %s ; tree: %s" % (self.actual_user.username, self.tree_view)

    def get_full_name(self):
        return self.__str__()


from paypal.standard.ipn.signals import payment_was_successful
import sys
from django.dispatch import receiver


def show_me_the_money(sender, **kwargs):
    print >>sys.stderr, 'Goodbye, cruel world!'
    #ipn_obj = sender
    # Undertake some action depending upon `ipn_obj`.
    #if ipn_obj.custom == "Upgrade all users!":
        #pass
        #Users.objects.update(paid=True)

payment_was_successful.connect(show_me_the_money)
