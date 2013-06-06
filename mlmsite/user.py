# ----- TASK TASK00002 START -----
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

import models


class User(models.UserModel):
    """Defines the user. At creation, it also saves the user to the database.
       It translates database and django exceptions to readable ones."""

    # -------------------------------------------------------------------------
    # The exceptions
    class EmailAlreadyExists:
        """Signals that an user with that email already exists"""
        pass

    # -------------------------------------------------------------------------
    class EmailWronglyFormatted:
        """Signals that an email address has invalid format"""
        pass

    # -------------------------------------------------------------------------
    class EmailTooLong:
        """Signals that an email address is too long"""
        pass

    # -------------------------------------------------------------------------
    # The methods
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

        # Save user to database, and do the proper checks.
        try:
            # This validates the model:
            super(User, self).full_clean()
            # This commits the model to the database
            super(User, self).save()
        except ValidationError as err:
            # The specified ValidationError below raises if the email address
            # is not unique.
            if err.message_dict == {'email': [_(u'M\xe1r l\xe9tezik User model ilyennel: Email.')]}:
                raise self.EmailAlreadyExists
            elif err.message_dict == {'email': [_(u'\xcdrjon be egy \xe9rv\xe9nyes e-mail c\xedmet.')]}:
                raise self.EmailWronglyFormatted
            elif err.message_dict['email'][0].startswith(_(u'Bizonyosodjon meg arr\xf3l, hogy ez az \xe9rt\xe9k legfeljebb')):
                raise self.EmailTooLong
            else:
                raise
# ----- TASK TASK00002 END -----
