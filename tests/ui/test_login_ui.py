import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage


@pytest.mark.parametrize("email, password, name, account, email_error, password_error, general_error", [
    ("admin@practicesoftwaretesting.com", "welcome01", "John Doe", "Sales over the years", None, None, None),
    ("customer@practicesoftwaretesting.com", "welcome01", "Jane Doe", "My account", None, None, None),
    ("customer2@practicesoftwaretesting.com", "welcome01", "Jack Howe", "My account", None, None, None),
    ("", "", None, None, "Email is required", "Password is required", None),
    ("", "welcome01", None, None, "Email is required", None, None),
    ("customer2@practicesoftwaretesting.com", "", None, None, None, "Password is required", None),
    ("customer2practicesoftwaretestingcom", "welcome01", None, None, "Email format is invalid", None, None),
    ("customer2@practicesoftwaretesting.com", "w", None, None, None, "Password length is invalid", None),
    ("cusomer2@pr.com", "welcome01", None, None, None, None, "Invalid email or password"),
    ("customer2@practicesoftwaretesting.com", "welcomdddddde01", None, None, None, None, "Invalid email or password")
])
def test_login(browser, email, password, name, account, email_error, password_error, general_error):
    home_page = HomePage(browser)
    home_page.navigate_to_login()
    login_page = LoginPage(browser)
    login_page.login(email, password)
    if name and account:
        name_text, account_text = login_page.is_login()
        assert account in account_text, f"Expected '{account}' but got '{account_text}'"
        assert name in name_text, f"Expected '{name}' but got '{name_text}'"
    else:
        if email_error:
            assert email_error in login_page.email_alert(), f"Expected email error '{email_error}', but got '{login_page.email_alert()}'"
        if password_error:
            assert password_error in login_page.password_alert(), f"Expected email error '{password_error}', but got '{login_page.password_alert()}'"
        if general_error:
            actual_general_error = login_page.general_alert()

            # Allow either 'Invalid email or password' OR 'Account locked, too many failed attempts'
            allowed_errors = ["Invalid email or password",
                              "Account locked, too many failed attempts. Please contact the administrator."]
            assert actual_general_error in allowed_errors, f"Expected '{general_error}', but got '{actual_general_error}'"
