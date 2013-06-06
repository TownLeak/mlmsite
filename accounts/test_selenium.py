from django.utils import unittest
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class TestSelenium(LiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(TestSelenium, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(TestSelenium, cls).tearDownClass()

    def test_login(self):
        pass
        # self.selenium.get('%s%s' % (self.live_server_url, ''))
        # username_input = self.selenium.find_element_by_name("identification")
        # username_input.send_keys('myuser')
        # password_input = self.selenium.find_element_by_name("password")
        # password_input.send_keys('secret')
        # self.selenium.find_element_by_xpath('//input[@value="Signin"]').click()


# -----------------------------------------------------------------------------
def TheTestSuite():
    return unittest.TestLoader().loadTestsFromTestCase(TestSelenium)
