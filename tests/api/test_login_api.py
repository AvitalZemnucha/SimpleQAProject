import requests
import pytest
from utils.helpers import api_login_user
from utils.config import Config


@pytest.mark.parametrize("email, password, expected_first_name, expected_last_name, expected_email",
                         [
                             (Config.USER_ACCOUNT["email"], Config.USER_ACCOUNT["password"], "Jane", "Doe",
                              "customer@practicesoftwaretesting.com"),
                             (Config.USER2_ACCOUNT["email"], Config.USER2_ACCOUNT["password"], "Jack", "Howe",
                              "customer2@practicesoftwaretesting.com"),
                             (Config.ADMIN_ACCOUNT["email"], Config.ADMIN_ACCOUNT["password"], "John", "Doe",
                              "admin@practicesoftwaretesting.com")
                         ]
                         )
def test_login_user_api(api_session, email, password, expected_first_name, expected_last_name, expected_email):
    login_successful = api_login_user(api_session, email, password, 200)
    assert login_successful, "Login Failed!"

    # After successful login, get the user details
    response = api_session.get(Config.API_AFTER_LOGIN)
    assert response.status_code == 200, f"Failed to get user details. Status code: {response.status_code}"

    # Validate the response data for each user
    data = response.json()
    assert data[
               'first_name'] == expected_first_name, f"Expected first name {expected_first_name}, but got {data['first_name']}"
    assert data[
               'last_name'] == expected_last_name, f"Expected last name {expected_last_name}, but got {data['last_name']}"
    assert data['email'] == expected_email, f"Expected email {expected_email}, but got {data['email']}"
