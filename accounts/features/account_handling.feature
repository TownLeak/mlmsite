Feature: Users can handle their accounts.

    Scenario: Non-existing user successfully signs up
        Given The username "atyala" does not exists
        When I go to the "/accounts/signup" URL
        And I fill the field "username" with "atyala"
        And I fill the field "email" with "patyala@foobar.com"
        And I fill the field "password1" with "p1"
        And I fill the field "password2" with "p1"
        And I fill the field "first_name" with "Zsolt"
        And I fill the field "last_name" with "Molnar"
        And I select the field "birth_date_year" with "1970"
        And I select the field "birth_date_day" with "1"
        And I select the field "birth_date_month" with "1"
        And I fill the field "Postal-address" with "Addrss 1"
        And I fill the field "Postal-city" with "City 1"
        And I fill the field "Postal-zip_code" with "12345"
        And I select the field "Postal-country" with "HU"
        And I fill the field "Delivery-address" with "Addrss 1"
        And I fill the field "Delivery-city" with "City 1"
        And I fill the field "Delivery-zip_code" with "12345"
        And I select the field "Delivery-country" with "HU"
        And I click on "submit"
        Then I should see "Thank you for signing up with us!"
        Then email is sent to "patyala@foobar.com" with subject containing "Your signup at"

    Scenario: Existing user signs in
        Given The username "user1" exists
        When I go to the "/" URL
        And I fill the field "identification" with "user1"
        And I fill the field "password" with "a"
        And I click on "login"
        Then I should see "View profile"
