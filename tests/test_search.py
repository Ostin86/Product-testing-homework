import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from decimal import Decimal
from typing import List

from pageobject.search_page import ProductInfo, SearchPage
from webdriver_factory import WebDriverFactory


class SearchPageTest(unittest.TestCase):
    search_request_text_apple: str = 'apple'
    search_request_text_sony: str = 'sony'
    search_request_text_nokia: str = 'nokia'
    product_name_apple: str = 'Apple Cinema 30"'
    product_price_apple: Decimal = Decimal('110.00')
    product_name_sony: str = 'Sony VAIO'
    product_price_sony: Decimal = Decimal('1202.00')
    text_without_search_results: str = 'There is no product that matches the search criteria.'
    search_request_in_search_criteria_field: str = 'stunning'
    expected_multiple_search_results: list = ['HP LP3065', 'iMac']

    def setUp(self) -> None:
        """Действия до теста"""
        self.driver = self.driver = WebDriverFactory.get_driver()
        self.search_page = SearchPage(self.driver)
        self.search_page.open()
        self.search_page.clear_search_field()

    def tearDown(self):
        """Действия после теста"""
        self.driver.close()

    def test_search_results_with_apple_request(self):
        """Тест работы поискового запроса apple"""
        self.search_page.enter_search_request_in_search_field(self.search_request_text_apple)
        self.search_page.click_by_find_button()
        results = self.search_page.get_search_results()
        product_name: str = results[0].name
        product_price: Decimal = results[0].price
        self.assertEqual((product_name, product_price), (self.product_name_apple, self.product_price_apple))

    def test_search_results_with_sony_request(self):
        """Тест работы поискового запроса sony"""
        self.search_page.enter_search_request_in_search_field(self.search_request_text_sony)
        self.search_page.click_by_find_button()
        results = self.search_page.get_search_results()
        product_name: str = results[0].name
        product_price: Decimal = results[0].price
        self.assertEqual((product_name, product_price), (self.product_name_sony, self.product_price_sony))

    def test_search_results_with_nokia_request(self):
        """Тест работы поискового запроса nokia"""
        self.search_page.enter_search_request_in_search_field(self.search_request_text_nokia)
        self.search_page.click_by_find_button()
        actual_results = self.search_page.get_text_about_product_that_doesnt_exist()
        expected_results: str = self.text_without_search_results
        self.assertEqual(actual_results, expected_results)

    def test_search_results_by_search_criteria(self):
        """Тест работы поискового запроса с использованием поисковых критериев"""
        self.search_page.enter_search_request_in_search_criteria_field(self.search_request_in_search_criteria_field)
        self.search_page.click_by_search_in_product_description_checkbox()
        self.search_page.click_by_search_button()
        actual_results = self.search_page.get_search_results()
        actual_results_names: List[str] = [actual_results[0].name, actual_results[1].name]
        expected_results: List[str] = self.expected_multiple_search_results
        self.assertEqual(actual_results_names, expected_results)
