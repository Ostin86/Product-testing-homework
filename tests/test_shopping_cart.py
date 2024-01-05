import unittest
from decimal import Decimal
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pageobject.shopping_cart_page import ShoppingCart
from pageobject.product_page import ProductPage


class ShoppingCartTest(unittest.TestCase):

    def setUp(self):
        """Действия до теста"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.first_product_id: str = '33'
        self.second_product_id: str = '47'
        self.samsung_product_amount: int = 2
        self.successful_adding_samsung_product_to_cart_message: str = (
            'Success: You have added Samsung SyncMaster 941BW to your '
            'shopping cart!')
        self.successful_adding_hp_product_to_cart_message: str = 'Success: You have added HP LP3065 to your shopping cart!'
        self.expected_total_cost: Decimal = Decimal('606.00')
        self.expected_first_product_name: str = 'Samsung SyncMaster 941BW'
        self.expected_second_product_name: str = 'HP LP3065'
        self.text_for_empty_shopping_cart: str = 'Your shopping cart is empty!'

    def tearDown(self):
        self.driver.close()

    def test_adding_necessary_amount_product_into_cart(self):
        """Тест на добавление необходимого количества одного товара в корзину"""
        shopping_cart_page = ShoppingCart(self.driver)
        product_url = ProductPage(self.driver, self.first_product_id).get_product_url()
        shopping_cart_page.open_product_to_cart_adding(product_url)
        shopping_cart_page.clear_quantity_field()
        shopping_cart_page.add_amount_of_products_in_quantity_field(self.samsung_product_amount)
        shopping_cart_page.click_on_add_to_cart_button()
        shopping_cart_page.wait_comparison_adding_success_message()
        actual_result: str = shopping_cart_page.get_success_message_text().strip('\n×')
        expected_result: str = self.successful_adding_samsung_product_to_cart_message
        self.assertEqual(actual_result, expected_result)

    def test_adding_one_product_into_shopping_cart(self):
        """Тест на добавление одного товара в корзину"""
        shopping_cart_page = ShoppingCart(self.driver)
        product_url = ProductPage(self.driver, self.second_product_id).get_product_url()
        shopping_cart_page.open_product_to_cart_adding(product_url)
        shopping_cart_page.click_on_add_to_cart_button()
        shopping_cart_page.wait_comparison_adding_success_message()
        actual_result: str = shopping_cart_page.get_success_message_text().strip('\n×')
        expected_result: str = self.successful_adding_hp_product_to_cart_message
        self.assertEqual(actual_result, expected_result)

    def test_adding_several_products_into_shopping_cart(self):
        """Тест на добавление нескольких различных товаров в корзину"""
        shopping_cart_page = ShoppingCart(self.driver)
        first_product_url = ProductPage(self.driver, self.first_product_id).get_product_url()
        second_product_url = ProductPage(self.driver, self.second_product_id).get_product_url()
        shopping_cart_page.open_product_to_cart_adding(first_product_url)
        shopping_cart_page.clear_quantity_field()
        shopping_cart_page.add_amount_of_products_in_quantity_field(self.samsung_product_amount)
        shopping_cart_page.click_on_add_to_cart_button()
        shopping_cart_page.open_product_to_cart_adding(second_product_url)
        shopping_cart_page.click_on_add_to_cart_button()
        shopping_cart_page.open_checkout_cart_url()
        actual_total_cost: Decimal = shopping_cart_page.get_total_sum_in_shopping_cart()
        actual_first_product_name_text: str = shopping_cart_page.get_first_product_name()
        actual_second_product_name_text: str = shopping_cart_page.get_second_product_name()
        self.assertEqual((actual_total_cost, actual_first_product_name_text, actual_second_product_name_text),
                         (self.expected_total_cost, self.expected_first_product_name,
                          self.expected_second_product_name))

    def test_removing_products_from_shopping_cart(self):
        """Тест на удаление товаров из корзины"""
        shopping_cart_page = ShoppingCart(self.driver)
        first_product_url = ProductPage(self.driver, self.first_product_id).get_product_url()
        second_product_url = ProductPage(self.driver, self.second_product_id).get_product_url()
        shopping_cart_page.open_product_to_cart_adding(first_product_url)
        shopping_cart_page.clear_quantity_field()
        shopping_cart_page.add_amount_of_products_in_quantity_field(self.samsung_product_amount)
        shopping_cart_page.click_on_add_to_cart_button()
        shopping_cart_page.open_product_to_cart_adding(second_product_url)
        shopping_cart_page.click_on_add_to_cart_button()
        shopping_cart_page.open_checkout_cart_url()
        shopping_cart_page.click_on_remove_buttons()
        actual_result = shopping_cart_page.get_text_for_empty_shopping_cart()
        expected_result = self.text_for_empty_shopping_cart
        self.assertEqual(actual_result, expected_result)

