import unittest
from django.test import TestCase
from paypal.standard.ipn.signals import payment_was_successful
from mlmsite.models import show_me_the_money


def SimpleReceiver(sender, **kwargs):
    obj = kwargs['object']
    obj._signalReceived = True
    obj.assertEqual(sender, "Sender")


class Tests(TestCase):
    def setUp(self):
        self._signalReceived = False
        payment_was_successful.disconnect(show_me_the_money)

    def testConnectingSignals(self):
        payment_was_successful.connect(SimpleReceiver)
        self.assertFalse(self._signalReceived)
        payment_was_successful.send(sender="Sender", message="Hello", level=1, object=self)
        self.assertTrue(self._signalReceived)
        # test disconnect signal
        self._signalReceived = False
        payment_was_successful.disconnect(SimpleReceiver)
        payment_was_successful.send(sender="Sender", message="Hello", level=1, object=self)
        self.assertFalse(self._signalReceived)

    def testConnectPaypalSignalReceiver(self):
        payment_was_successful.connect(show_me_the_money)

        class ipn_obj:
            custom = 'atyala'

        payment_was_successful.send(sender=ipn_obj, message="Hello", level=1, object=self)


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(Tests)
