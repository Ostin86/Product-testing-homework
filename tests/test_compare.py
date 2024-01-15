import unittest
from typing import List


from pageobject.compare_page import ComparePage
from pageobject.product_page import ProductPage
from webdriver_factory import WebDriverFactory


class CompareTest(unittest.TestCase):
    driver = None
    first_product_id = '42'
    second_product_id = '33'
    success_text_after_adding_to_comparison_apple_product: str = 'Success'
    expected_product_ids: list = ['42', '33']
    expected_products_names: List[str] = ['Apple Cinema 30"', 'Samsung SyncMaster 941BW']
    text_when_there_are_not_any_product_in_compare_list: str = 'You have not chosen any products to compare.'

    @classmethod
    def setUpClass(cls) -> None:
        """Предустановка. Выполняется один раз перед всеми тестами"""
        cls.driver = WebDriverFactory.get_driver()
        cls.product_page_for_the_first_product = ProductPage(cls.driver, cls.first_product_id)
        cls.product_page_for_the_second_product = ProductPage(cls.driver, cls.second_product_id)
        cls.compare_page = ComparePage(cls.driver)

    def setUp(self):
        """Действия до теста"""
        self.product_page_for_the_first_product.open()
        self.product_page_for_the_first_product.click_on_compare_this_product_button()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()

    def test_adding_product_to_comparison_list(self):
        """Тест на успешное добавление продукта в список сравнения"""
        actual_result_text = self.product_page_for_the_first_product.get_comparison_adding_success_message()
        expected_result_text = self.success_text_after_adding_to_comparison_apple_product
        self.assertTrue(expected_result_text in actual_result_text)

    def test_compare_two_products(self):
        """Тест на сравнение двух продуктов"""
        self.product_page_for_the_second_product.open()
        self.product_page_for_the_second_product.click_on_compare_this_product_button()
        self.product_page_for_the_second_product.click_on_product_comparison_link()
        actual_products_texts: List[str] = self.compare_page.get_added_to_comparison_products_names()
        self.assertEqual(self.expected_products_names, actual_products_texts)

    def test_clearing_comparison_list(self):
        """Тест на возможность удаления продуктов со списка сравнения"""
        self.product_page_for_the_second_product.open()
        self.product_page_for_the_second_product.click_on_compare_this_product_button()
        self.product_page_for_the_second_product.click_on_product_comparison_link()
        self.compare_page.clear_comparison_list(self.expected_product_ids)
        self.compare_page.get_no_one_elements_in_comparison_list_text()
        expected_result = self.text_when_there_are_not_any_product_in_compare_list
        actual_result = self.compare_page.get_no_one_elements_in_comparison_list_text()
        self.assertEqual(expected_result, actual_result)
