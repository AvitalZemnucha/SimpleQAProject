import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.logout_page import LogoutPage


@pytest.mark.parametrize("email, password, name, account", [
    ("admin@practicesoftwaretesting.com", "welcome01", "John Doe", "Sales over the years"),
    ("customer@practicesoftwaretesting.com", "welcome01", "Jane Doe", "My account"),
    ("customer2@practicesoftwaretesting.com", "welcome01", "Jack Howe", "My account")
])
def test_login_and_then_logout(browser, email, password, name, account):
    home_page = HomePage(browser)
    home_page.navigate_to_login()
    login_page = LoginPage(browser)
    login_page.login(email, password)
    name_text, account_text = login_page.is_login()
    assert account in account_text, f"Expected '{account}' but got '{account_text}'"
    assert name in name_text, f"Expected '{name}' but got '{name_text}'"
    logout_page = LogoutPage(browser)
    logout_page.logout()
    sign_in_text, login_text = logout_page.is_logged_out()
    assert "Login" in login_text, f"Expected 'Login' but got '{login_text}'"
    assert "Sign in" in sign_in_text, f"Expected 'Sign in' but got '{sign_in_text}'"
