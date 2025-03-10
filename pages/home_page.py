import time

from selenium.common import TimeoutException

from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


class HomePage(BasePage):
    SIGNIN_BUTTON = (By.CSS_SELECTOR, ".nav-link[data-test='nav-sign-in']")
    CATEGORY_CHECKBOXES = (By.XPATH,
                           "//input[starts-with(@data-test, 'category-') and contains(translate(ancestor::label/text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'hammer')]")

    FILTER_COMPLETED = (By.XPATH, "//div[@data-test='filter_completed']")
    # FILTER_COMPLETED = (By.CSS_SELECTOR, "[data-test='sorting_completed']")

    FIRST_RESULT = (By.XPATH, "//a[starts-with(@data-test, 'product-')]")
    BRAND_CHECKBOX_STRATEGIES = [
        (By.XPATH, "//input[starts-with(@data-test, 'brand-')]"),
        (By.XPATH, "//input[@name='brand_id']"),
        (By.XPATH, "//input[contains(@class, 'brand-checkbox')]")
    ]

    SEARCH_BOX = (By.ID, "search-query")
    SEARCH_RESULT_TITLE = (By.XPATH, "//h3")

    LEFT_SLIDER = (By.CSS_SELECTOR, "span[ngxsliderhandle].ngx-slider-pointer-min")
    RIGHT_SLIDER = (By.CSS_SELECTOR, "span[ngxsliderhandle].ngx-slider-pointer-max")

    PRODUCT_PRICE = (By.XPATH, "//span[@data-test='product-price']")

    SLIDER_FILTERED_LIST = (By.CSS_SELECTOR, ".col-md-9")
    PRICE_SLIDER_FIRST_ITEM = (By.XPATH, "(//div[@class='card-footer']//span[@data-test='product-price'])[1]")
    SORT_ITEMS = (By.CSS_SELECTOR, "select[data-test='sort']")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, "[data-test^='product-']")
    FIRST_PRODUCT_NAME = (By.XPATH, "(//a[starts-with(@data-test, 'product-')])[1]")

    def navigate_to_login(self):
        self.driver.find_element(*self.SIGNIN_BUTTON).click()

    def filter_by_category(self, category_index=0):
        checkboxes = self.wait_for_all_elements(self.CATEGORY_CHECKBOXES)

        if not checkboxes or category_index >= len(checkboxes):
            raise Exception("No category checkbox found or index out of range")

        checkbox = checkboxes[category_index]
        self.driver.execute_script("arguments[0].scrollIntoView();", checkbox)
        checkbox.click()

        self.wait_for_all_elements(self.FILTER_COMPLETED)

        first_product = self.driver.find_elements(*self.FIRST_RESULT)
        if not first_product:
            raise Exception("No product found after filtering")

        return first_product[0].text

    def get_first_product_name(self):
        first_product = self.wait_for_element_visible(self.FIRST_RESULT)
        return first_product.text

    def get_brand_name(self):

        for locator in self.BRAND_CHECKBOX_STRATEGIES:
            try:
                brand_checkboxes = self.wait_for_all_elements(locator)

                if not brand_checkboxes:
                    continue  # Try the next locator if none found

                # Pick the first available brand
                first_checkbox = brand_checkboxes[0]
                label = first_checkbox.find_element(By.XPATH, "./ancestor::label")
                selected_brand = label.text.strip()

                # Scroll into view and click
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_checkbox)
                first_checkbox.click()

                # Wait for filter to apply
                self.wait_for_all_elements(self.FILTER_COMPLETED)

                print(f"Selected brand: {selected_brand}")
                return selected_brand  # Return the selected brand for assertion in tests

            except Exception:
                continue

        raise Exception("No brand checkboxes found!")

    def search_tool(self, tool):
        tool_element = self.wait_for_element_visible(self.SEARCH_BOX)
        tool_element.send_keys(tool)
        tool_element.send_keys(Keys.RETURN)
        search_assert = self.wait_for_element_visible(self.SEARCH_RESULT_TITLE)
        return search_assert.text

    def filter_by_price_range(self, min_price, max_price):
        """Adjusts the price range slider dynamically to filter products."""

        left_slider = self.wait_for_element_visible(self.LEFT_SLIDER)
        right_slider = self.wait_for_element_visible(self.RIGHT_SLIDER)

        # Get the slider track width (total range)
        slider_track = self.driver.find_element(By.CSS_SELECTOR, "ngx-slider")
        track_width = slider_track.size["width"]

        # Calculate how much to move the sliders
        max_price_value = 200  # Set this based on the slider's max value
        min_offset = (min_price / max_price_value) * track_width
        max_offset = ((max_price_value - max_price) / max_price_value) * track_width

        actions = ActionChains(self.driver)

        try:
            # Move Left Slider to min_price
            actions.click_and_hold(left_slider).move_by_offset(min_offset, 0).release().perform()

            # Move Right Slider to max_price
            actions.click_and_hold(right_slider).move_by_offset(max_offset, 0).release().perform()

            # Wait for filter update
            self.wait_for_all_elements(self.FILTER_COMPLETED)

        except Exception as e:
            raise Exception(f"Error adjusting price range: {e}")

    def verify_price_range(self, min_price, max_price):
        # Verify that all product prices are within the specified range
        prices = self.wait_for_all_elements(self.PRODUCT_PRICE)
        for price_element in prices:
            price_text = price_element.text.strip().replace('$', '').replace(',', '')
            try:
                price = float(price_text)
                if not (min_price <= price <= max_price):
                    raise AssertionError(f"Price {price} is not within the range of ${min_price} to ${max_price}")
            except ValueError:
                raise Exception(f"Invalid price format: {price_text}")

        print(f"All product prices are between ${min_price} and ${max_price}")
        return True

    def sort_items(self, sort_value):
        sort_select = Select(self.wait_for_element_visible(self.SORT_ITEMS))
        sort_select.select_by_value(sort_value)
        self.wait_for_all_elements(self.PRODUCT_ITEMS)
        time.sleep(1)
        print("Sorting completed successfully.")
