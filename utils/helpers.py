import requests
import pytest
from utils.config import Config


def api_login_user(api_session, email, password, expected_status_code):
    url = f"{Config.API_BASE_URL}users/login"
    payload = {
        "email": email,
        "password": password
    }
    response = api_session.post(url, json=payload)
    if response.status_code == expected_status_code:
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            assert access_token is not None, "No access token found in response"
            api_session.headers.update({"Authorization": f"Bearer {access_token}"})
            print(f"Access token successfully added for {email}: {access_token}")  # Debugging line
        return True
    else:
        print(f"Login failed for {email} with status code: {response.status_code}")
        print(f"Response: {response.text}")  # Log the response body
        return False
