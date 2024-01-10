import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pageobject.compare_page import ComparePage
from pageobject.product_page import ProductPage
from webdriver_factory import WebDriverFactory


class CompareTest(unittest.TestCase):
    first_product_id = '42'
    second_product_id = '33'
    success_text_after_adding_to_comparison_apple_product: str = 'Success'
    expected_text_about_apple_added_product: str = 'Apple Cinema 30"'
    expected_text_about_samsung_added_product: str = 'Samsung SyncMaster 941BW'
    text_when_there_are_not_any_product_in_compare_list: str = 'You have not chosen any products to compare.'

    def setUp(self):
        """Действия до теста"""
        self.driver = self.driver = WebDriverFactory.get_driver()
        self.product_page = ProductPage(self.driver, self.first_product_id)
        self.product_page.open()
        self.product_page.click_on_compare_this_product_button()

    def tearDown(self):
        self.driver.close()

    def test_adding_product_to_comparison_list(self):
        """Тест на успешное добавление продукта в список сравнения"""
        actual_result_text = self.product_page.get_comparison_adding_success_message()
        expected_result_text = self.success_text_after_adding_to_comparison_apple_product
        self.assertTrue(expected_result_text in actual_result_text)

    def test_compare_two_products(self):
        """Тест на сравнение двух продуктов"""
        product_page = ProductPage(self.driver, self.second_product_id)
        product_page.open()
        product_page.click_on_compare_this_product_button()
        product_page.click_on_product_comparison_link()
        elements_with_product_names: list = ComparePage(self.driver).get_added_to_comparison_products()
        actual_text_about_apple_added_product: str = elements_with_product_names[0].text
        actual_text_about_samsung_added_product: str = elements_with_product_names[1].text
        self.assertEqual((actual_text_about_apple_added_product, actual_text_about_samsung_added_product),
                         (self.expected_text_about_apple_added_product, actual_text_about_samsung_added_product))

    def test_clearing_comparison_list(self):
        """Тест на возможность удаления продуктов со списка сравнения"""
        product_page = ProductPage(self.driver, self.second_product_id)
        product_page.open()
        product_page.click_on_compare_this_product_button()
        product_page.click_on_product_comparison_link()
        compare_page = ComparePage(self.driver)
        compare_page.click_on_remove_buttons()
        compare_page.get_text_when_no_one_elements_in_comparison_list()
        expected_result = self.text_when_there_are_not_any_product_in_compare_list
        actual_result = compare_page.get_text_when_no_one_elements_in_comparison_list()
        self.assertEqual(expected_result, actual_result)
