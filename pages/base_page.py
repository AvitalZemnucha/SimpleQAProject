from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_element_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_all_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def wait_for_products_update(self, product_locator, timeout=10):
        """Wait until product prices update (used after applying filters)."""
        try:
            old_products = self.driver.find_elements(*product_locator)
            old_count = len(old_products)

            def products_updated(driver):
                new_products = driver.find_elements(*product_locator)
                return len(new_products) != old_count  # Return True if product count changes

            self.wait.until(products_updated)
        except TimeoutException:
            raise Exception("Product list did not update after filtering!")
