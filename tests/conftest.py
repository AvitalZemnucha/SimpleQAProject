import pytest
from selenium import webdriver
import requests
from utils.config import Config
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(Config.BASE_URL)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    yield session
