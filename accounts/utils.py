import datetime
from config import Config


# -----------------------------------------------------------------------------
class DateTimeFactory:
    """
    Today and now, based on server's defined locale.

    A subclass may apply different rules for determining "today".
    For example, the broswer's time-zone could be used instead of the
    server's timezone.
    """
    @classmethod
    def getToday(cls):
        """Return today as date object."""
        return datetime.date.today()


# -----------------------------------------------------------------------------
class MinAgeFactory:
    """
    Dependency returning the minimal accepted age. Necessary for testing,
    to be able to test with fixtures.
    """
    @classmethod
    def getMinAge(cls):
        """
        Return the entity providing the minimal age of the users.
        """
        return Config.min_age
