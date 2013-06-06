from lettuce import step, world
from lettuce.django import django_url
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from lettuce.django import mail
from nose.tools import assert_equals, assert_in
import re


@step(u'When I go to the "(.*)" URL')
def when_i_go_to_the_accounts_signup_url(step, url):
    world.response = world.browser.visit(django_url(url))


@step(u'The username "(.*)" does not exists')
def a_user_does_not_exists_with_username(step, p_username):
    try:
        user = User.objects.get(username=p_username)
    except User.DoesNotExist:
        return


@step(u'Given The username "([^"]*)" exists')
def given_the_username_group1_exists(step, username):
    return not a_user_does_not_exists_with_username(step, username)


@step(u'And I fill the field "(.*)" with "(.*)"')
def i_fill_in(step, field, value):
    world.browser.fill(field, value)


@step(u'And I select the field "([^"]*)" with "([^"]*)"')
def and_i_select_the_field_group1_with_group2(step, group1, group2):
    world.browser.select(group1, group2)


@step(u'And I click on "([^"]*)"')
def and_i_click_on_group1(step, button_name):
    button = world.browser.find_by_name(button_name)[0]
    #assert_equals()
    button.click()


@step(u'I should see "(.*)"')
def i_should_see(step, text):
    assert text in world.browser.html


@step(u'Then email is sent to "([^"]*)" with subject containing "([^"]*)"')
def then_email_is_sent_to_group1_with_subject_containing_group2(step, to, subject):
    # It seems that the mail.queue is a global message queue, and error messages (page not found, etc.) also get here.
    # This is a hack below, as there are resources not found. If I fix those problems, I can remove the extra lines.
    message = mail.queue.get(True, timeout=5)
    message = mail.queue.get(True, timeout=5)
    message = mail.queue.get(True, timeout=5)
    assert_in(subject, message.subject)
    assert_equals(message.recipients(), [to])
    world.email_body = message.body


@step(u'And I activate the account')
def and_i_activate_the_account(step):
    activation_url = re.findall(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        world.email_body
    )[0]

    world.response = world.browser.visit(activation_url)
