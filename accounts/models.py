import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from userena.models import UserenaLanguageBaseProfile
from django_countries import CountryField

from utils import DateTimeFactory, MinAgeFactory


# -----------------------------------------------------------------------------
class Dependencies:
    """
    Dependency injector for AdultBirthDateField classes.
    """
    dateTimeFactory = DateTimeFactory
    minAgeFactory = MinAgeFactory


# -------------------------------------------------------------------------
class AgeError(ValidationError):
    """
    Encapsulates age error: raised when the user is not an adult. It is
    a ValidationError with a special message.
    """

    def __init__(self, deps=Dependencies()):
        msg = _(u"You must be min %d years old." % deps.minAgeFactory.getMinAge())
        super(AgeError, self).__init__(msg)


# -----------------------------------------------------------------------------
class AdultBirthDateField(models.DateField):
    """
    Birth date for adults. It checks if the birth date corresponds to an
    adult, i.e the person with such a birth date is older than min_age (18).
    """

    # Explanation of this: http://bit.ly/10ykL4G
    __metaclass__ = models.SubfieldBase

    # -------------------------------------------------------------------------
    def isAdultValidator(self, birthdate):
        """
        Check if a birth date corresponds to an adult.

        Attribute: birthdate
        The birth date. It is a Python datetime.date object, seems to be after
        clean. So, we can do some math with it...
        """
        today = self.deps.dateTimeFactory.getToday()
        year = today.year - self.deps.minAgeFactory.getMinAge()
        min_birthday = datetime.date(year, today.month, today.day)
        diff = birthdate.toordinal() - min_birthday.toordinal()

        if diff > 0:
            raise AgeError()

    # -------------------------------------------------------------------------
    def __init__(self, deps=Dependencies(), *args, **kwargs):
        self.deps = deps
        kwargs['verbose_name'] = _(u'Birth date')
        kwargs['validators'] = [self.isAdultValidator]
        kwargs['blank'] = False
        kwargs['null'] = True
        super(AdultBirthDateField, self).__init__(*args, **kwargs)


# -----------------------------------------------------------------------------
class PostalAddress(models.Model):
    """
    Class representing postal address.
    """
    address = models.CharField(_(u"Address"), max_length=256)
    city = models.CharField(_(u"City"), max_length=64, default="Budapest")
    state = models.CharField(_(u"State or province"), max_length=64, blank=True)
    zip_code = models.CharField(_(u"zip code"), max_length=16)
    country = CountryField()

    def __unicode__(self):
        if not self.state:
            state = "N/A"

        return "%s %s, %s, %s %s, %s" % (self.zip_code, self.city, self.address_1, self.address_2, state, self.country)


# -----------------------------------------------------------------------------
class UserProfile(UserenaLanguageBaseProfile):
    """
    The user profile model, attached to the user.

    Attribute: birth_date
    Birth date of the user.
    """

    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_(u'User Profile'),
                                related_name='user_profile')

    birth_date = AdultBirthDateField()

    postal_address = models.ForeignKey(
        PostalAddress,
        verbose_name=_(u'Postal address'),
        related_name='user_profile_postal_address',
        null=True
    )

    delivery_address = models.ForeignKey(
        PostalAddress,
        verbose_name=_(u'Delivery address'),
        related_name='user_profile_delivery_address',
        null=True
    )
