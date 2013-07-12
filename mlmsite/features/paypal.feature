Feature: Standard payment with Paypal.

    Scenario: User clicks on "pay" button
        Go to the "/try_paypal/" URL
        Click on "submit"
        I should see "Choose a way to pay"
        Click on "login_button"
        I should see "PayPal password"
        Fill the field "login_email" with "buyer@zsoltmolnar.hu"
        Fill the field "login_password" with "atyalapatyala"
        Click on "login.x"
        I should see "Vérifiez vos informations"
        Click on "continue"
        I should see "Merci de votre commande"
