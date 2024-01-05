import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from decimal import Decimal
from typing import List

from pageobject.search_page import ProductInfo, SearchPage


class SearchPageTest(unittest.TestCase):

    def setUp(self) -> None:
        """Действия до теста"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.search_request_text_apple: str = 'apple'
        self.search_request_text_sony: str = 'sony'
        self.search_request_text_nokia: str = 'nokia'
        self.product_name_apple: str = 'Apple Cinema 30"'
        self.product_price_apple: Decimal = Decimal('110.00')
        self.product_name_sony: str = 'Sony VAIO'
        self.product_price_sony: Decimal = Decimal('1202.00')
        self.text_without_search_results: str = 'There is no product that matches the search criteria.'
        self.search_request_in_search_criteria_field: str = 'stunning'
        self.expected_multiple_search_results: list = ['HP LP3065', 'iMac']

    def tearDown(self):
        """Действия после теста"""
        self.driver.close()

    def test_search_results_with_apple_request(self):
        """Тест работы поискового запроса apple"""
        search_page = SearchPage(self.driver)
        search_page.open()
        search_page.clear_search_field()
        search_page.enter_search_request_in_search_field(self.search_request_text_apple)
        search_page.click_by_find_button()
        results = search_page.get_search_results()
        product_name: str = results[0].name
        product_price: Decimal = results[0].price
        self.assertEqual((product_name, product_price), (self.product_name_apple, self.product_price_apple))

    def test_search_results_with_sony_request(self):
        """Тест работы поискового запроса sony"""
        search_page = SearchPage(self.driver)
        search_page.open()
        search_page.clear_search_field()
        search_page.enter_search_request_in_search_field(self.search_request_text_sony)
        search_page.click_by_find_button()
        results = search_page.get_search_results()
        product_name: str = results[0].name
        product_price: Decimal = results[0].price
        self.assertEqual((product_name, product_price), (self.product_name_sony, self.product_price_sony))

    def test_search_results_with_nokia_request(self):
        """Тест работы поискового запроса nokia"""
        search_page = SearchPage(self.driver)
        search_page.open()
        search_page.clear_search_field()
        search_page.enter_search_request_in_search_field(self.search_request_text_nokia)
        search_page.click_by_find_button()
        actual_results = search_page.get_text_about_product_that_doesnt_exist()
        expected_results: str = self.text_without_search_results
        self.assertEqual(actual_results, expected_results)

    def test_search_results_by_search_criteria(self):
        """Тест работы поискового запроса с использованием поисковых критериев"""
        search_page = SearchPage(self.driver)
        search_page.open()
        search_page.clear_search_criteria_field()
        search_page.enter_search_request_in_search_criteria_field(self.search_request_in_search_criteria_field)
        search_page.click_by_search_in_product_description_checkbox()
        search_page.click_by_search_button()
        actual_results = search_page.get_search_results()
        actual_results_names: List[str] = [actual_results[0].name, actual_results[1].name]
        expected_results: List[str] = self.expected_multiple_search_results
        self.assertEqual(actual_results_names, expected_results)
