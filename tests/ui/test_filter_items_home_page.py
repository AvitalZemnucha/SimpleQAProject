import pytest
from pages.home_page import HomePage


def test_filter_by_category_v1(browser):
    home_page = HomePage(browser)
    hammer_name = home_page.filter_by_category(0)
    assert "Hammer" in hammer_name


def test_filter_by_category_v2(browser):
    home_page = HomePage(browser)
    home_page.filter_by_category(0)  # Click the first category checkbox
    first_product_name = home_page.get_first_product_name()
    assert "Hammer" in first_product_name


def test_filter_by_brand(browser):
    home_page = HomePage(browser)
    home_page.get_brand_name()
    first_product_name = home_page.get_first_product_name()
    assert "Claw Hammer with Shock Reduction Grip" in first_product_name


def test_filter_by_search_box(browser):
    home_page = HomePage(browser)
    searched_product = home_page.search_tool("hammer")
    assert "Searched for: hammer" in searched_product


# @pytest.mark.parametrize("min_price, max_price", [(50, 100), (20, 200), (30, 150)])  # Example price ranges
# def test_filter_by_price_slider(browser, min_price, max_price):
#     home_page = HomePage(browser)
#     home_page.filter_by_price_range(min_price, max_price)
#     is_valid = home_page.verify_price_range(min_price, max_price)
#     assert is_valid, f"Some products have prices outside the ${min_price}-${max_price} range."

@pytest.mark.parametrize("sort_value, expected_value", [
    ("name,asc", "Adjustable Wrench"),  # Name (A - Z)
    ("name,desc", "Wood Saw"),  # Name (Z - A)
    ("price,desc", "Drawer Tool Cabinet"),  # Price (High - Low)
    ("price,asc", "Washers")  # Price (Low - High)

])
def test_sort_items(browser, sort_value, expected_value):
    home_page = HomePage(browser)
    home_page.sort_items(sort_value)
    first_product = home_page.get_first_product_name()
    assert expected_value in first_product
