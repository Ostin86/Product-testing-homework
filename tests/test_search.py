import unittest

from decimal import Decimal
from typing import List

from pageobject.search_page import SearchPage
from webdriver_factory import WebDriverFactory
from product_info_model import ProductInfo


class SearchPageTest(unittest.TestCase):
    driver = None
    apple_product = ProductInfo(name='Apple Cinema 30"', price=Decimal('110.00'))
    sony_product = ProductInfo(name='Sony VAIO', price=Decimal('1202.00'))
    search_request_text_apple: str = 'apple'
    search_request_text_sony: str = 'sony'
    search_request_text_nokia: str = 'nokia'
    text_without_search_results: str = 'There is no product that matches the search criteria.'
    search_request_in_search_criteria_field: str = 'stunning'
    expected_multiple_search_results: list = ['HP LP3065', 'iMac']

    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = WebDriverFactory.get_driver()
        cls.search_page = SearchPage(cls.driver)

    def setUp(self) -> None:
        """Действия до теста"""
        self.search_page.open()
        self.search_page.clear_search_field()

    @classmethod
    def tearDownClass(cls):
        """Действия после тестов"""
        cls.driver.quit()

    def test_search_results_with_apple_request(self):
        """Тест работы поискового запроса apple"""
        self.search_page.enter_search_request_in_search_field(self.search_request_text_apple)
        self.search_page.click_by_find_button()
        actual_search_results: List[ProductInfo] = self.search_page.get_search_results()
        expected_result = self.apple_product
        self.assertTrue(expected_result in actual_search_results)

    def test_search_results_with_sony_request(self):
        """Тест работы поискового запроса sony"""
        self.search_page.enter_search_request_in_search_field(self.search_request_text_sony)
        self.search_page.click_by_find_button()
        actual_search_results: List[ProductInfo] = self.search_page.get_search_results()
        expected_result = self.sony_product
        self.assertTrue(expected_result in actual_search_results)

    def test_search_results_with_nokia_request(self):
        """Тест работы поискового запроса nokia"""
        self.search_page.enter_search_request_in_search_field(self.search_request_text_nokia)
        self.search_page.click_by_find_button()
        actual_results = self.search_page.get_product_that_doesnt_exist_text()
        expected_results: str = self.text_without_search_results
        self.assertEqual(expected_results, actual_results)

    def test_search_results_by_search_criteria(self):
        """Тест работы поискового запроса с использованием поисковых критериев"""
        self.search_page.enter_search_request_in_search_criteria_field(self.search_request_in_search_criteria_field)
        self.search_page.click_by_search_in_product_description_checkbox()
        self.search_page.click_by_search_button()
        expected_result_names = self.expected_multiple_search_results
        actual_result_names = self.search_page.get_search_result_names()
        self.assertEqual(expected_result_names, actual_result_names)

