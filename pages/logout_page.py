from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LogoutPage(BasePage):
    LOG_OUT_MENU = (By.ID, "menu")
    SIGN_OUT = (By.XPATH, "//a[normalize-space()='Sign out']")
    SIGN_IN = (By.XPATH, "//a[normalize-space()='Sign in']")
    LOGIN_TITLE = (By.XPATH, "//h3[contains(text(), 'Login')]")

    def logout(self):
        self.wait_for_element_visible(self.LOG_OUT_MENU).click()
        self.wait_for_element_visible(self.SIGN_OUT).click()

    def is_logged_out(self):
        sign_in_element = self.wait_for_element_visible(self.SIGN_IN).text
        login_element = self.wait_for_element_visible(self.LOGIN_TITLE).text
        return sign_in_element, login_element
