from lettuce import step, world
from lettuce.django import django_url


@step(u'Go to the "(.*)" URL')
def when_i_go_to_url(step, url):
    world.response = world.browser.visit(django_url(url))


@step(u'Fill the field "(.*)" with "(.*)"')
def i_fill_in(step, field, value):
    world.browser.fill(field, value)


@step(u'Click on "([^"]*)"')
def and_i_click_on_button(step, button_name):
    button = world.browser.find_by_name(button_name)[0]
    button.click()


@step(u'I should see "(.*)"')
def i_should_see(step, text):
    assert text in world.browser.html
