import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pageobject.compare_page import ComparePage
from pageobject.product_page import ProductPage


class CompareTest(unittest.TestCase):

    def setUp(self):
        """Действия до теста"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.first_product_url = ProductPage(self.driver, '42').get_product_url()
        self.second_product_url = ProductPage(self.driver, '33').get_product_url()
        self.success_text_after_adding_to_comparison_apple_product: str = 'Success'
        self.expected_text_about_apple_added_product: str = 'Apple Cinema 30"'
        self.expected_text_about_samsung_added_product: str = 'Samsung SyncMaster 941BW'
        self.text_when_there_are_not_any_product_in_compare_list: str = 'You have not chosen any products to compare.'

    def tearDown(self):
        self.driver.close()

    def test_adding_product_to_comparison_list(self):
        """Тест на успешное добавление продукта в список сравнения"""
        compare_page = ComparePage(self.driver)
        compare_page.open_product_to_comparison_page(self.first_product_url)
        compare_page.click_on_compare_this_product_button()
        compare_page.wait_comparison_adding_success_message()
        actual_result_text = compare_page.get_comparison_adding_success_message()
        expected_result_text = self.success_text_after_adding_to_comparison_apple_product
        self.assertTrue(expected_result_text in actual_result_text)

    def test_compare_two_products(self):
        """Тест на сравнение двух продуктов"""
        compare_page = ComparePage(self.driver)
        compare_page.open_product_to_comparison_page(self.first_product_url)
        compare_page.wait_for_compare_this_product_button()
        compare_page.click_on_compare_this_product_button()
        compare_page.open_product_to_comparison_page(self.second_product_url)
        compare_page.click_on_compare_this_product_button()
        compare_page.wait_for_comparison_button()
        compare_page.click_on_product_comparison_link()
        elements_with_product_names: list = compare_page.get_added_to_comparison_products()
        actual_text_about_apple_added_product: str = elements_with_product_names[0].text
        actual_text_about_samsung_added_product: str = elements_with_product_names[1].text
        self.assertEqual((actual_text_about_apple_added_product, actual_text_about_samsung_added_product),
                         (self.expected_text_about_apple_added_product, actual_text_about_samsung_added_product))

    def test_clearing_comparison_list(self):
        """Тест на возможность удаления продуктов со списка сравнения"""
        compare_page = ComparePage(self.driver)
        compare_page.open_product_to_comparison_page(self.first_product_url)
        compare_page.click_on_compare_this_product_button()
        compare_page.open_product_to_comparison_page(self.second_product_url)
        compare_page.click_on_compare_this_product_button()
        compare_page.wait_for_comparison_button()
        compare_page.click_on_product_comparison_link()
        compare_page.click_on_remove_buttons()
        compare_page.get_text_when_no_one_elements_in_comparison_list()
        expected_result = self.text_when_there_are_not_any_product_in_compare_list
        actual_result = compare_page.get_text_when_no_one_elements_in_comparison_list()
        self.assertEqual(expected_result, actual_result)








