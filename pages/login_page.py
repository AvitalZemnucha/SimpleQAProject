from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CLASS_NAME, "btnSubmit")
    NAME = (By.XPATH, '//*[@id="menu"]')
    MY_ACCOUNT = (By.XPATH, "//h1")
    EMAIL_ALERT = (By.ID, "email-error")
    PASSWORD_ALERT = (By.ID, "password-error")
    GENERAL_ALERT = (By.XPATH, "//div[@class='help-block']")

    def login(self, email, password):
        self.wait_for_element_visible(self.EMAIL_INPUT).send_keys(email)
        self.wait_for_element_visible(self.PASSWORD_INPUT).send_keys(password)
        self.wait_for_element_clickable(self.LOGIN_BUTTON).click()

    def is_login(self):
        name_element = self.wait_for_element_visible(self.NAME).text
        account_element = self.wait_for_element_visible(self.MY_ACCOUNT).text
        return name_element, account_element

    def email_alert(self):
        email = self.wait_for_element_visible(self.EMAIL_ALERT).text
        return email

    def password_alert(self):
        password = self.wait_for_element_visible(self.PASSWORD_ALERT).text
        return password

    def general_alert(self):
        general = self.wait_for_element_visible(self.GENERAL_ALERT).text
        return general
