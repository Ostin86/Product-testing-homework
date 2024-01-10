import unittest
from decimal import Decimal

from pageobject.shopping_cart_page import ShoppingCart
from pageobject.product_page import ProductPage
from webdriver_factory import WebDriverFactory


class ShoppingCartTest(unittest.TestCase):
    first_product_id: str = '33'
    second_product_id: str = '47'
    samsung_product_amount: int = 2
    successful_adding_samsung_product_to_cart_message: str = (
        'Success: You have added Samsung SyncMaster 941BW to your '
        'shopping cart!')
    successful_adding_hp_product_to_cart_message: str = 'Success: You have added HP LP3065 to your shopping cart!'
    expected_total_cost: Decimal = Decimal('606.00')
    expected_first_product_name: str = 'Samsung SyncMaster 941BW'
    expected_second_product_name: str = 'HP LP3065'
    text_for_empty_shopping_cart: str = 'Your shopping cart is empty!'

    def setUp(self):
        """Действия до теста"""
        self.driver = WebDriverFactory.get_driver()

    def tearDown(self):
        self.driver.close()

    def test_adding_necessary_amount_product_into_cart(self):
        """Тест на добавление необходимого количества одного из товаров в корзину"""
        product_page = ProductPage(self.driver, self.first_product_id)
        product_page.open()
        product_page.clear_quantity_field()
        product_page.add_amount_of_products_in_quantity_field(self.samsung_product_amount)
        product_page.click_on_add_to_cart_button()
        actual_result: str = product_page.get_success_message_about_adding_product_into_shopping_cart_text().strip(
            '\n×')
        expected_result: str = self.successful_adding_samsung_product_to_cart_message
        self.assertEqual(actual_result, expected_result)

    def test_adding_one_product_into_shopping_cart(self):
        """Тест на добавление одного товара в корзину"""
        product_page = ProductPage(self.driver, self.second_product_id)
        product_page.open()
        product_page.click_on_add_to_cart_button()
        actual_result: str = product_page.get_success_message_about_adding_product_into_shopping_cart_text().strip(
            '\n×')
        expected_result: str = self.successful_adding_hp_product_to_cart_message
        self.assertEqual(actual_result, expected_result)

    def test_adding_several_products_into_shopping_cart(self):
        """Тест на добавление нескольких различных товаров в корзину"""
        first_product_page = ProductPage(self.driver, self.first_product_id)
        second_product_page = ProductPage(self.driver, self.second_product_id)
        shopping_cart_page = ShoppingCart(self.driver)
        first_product_page.open()
        first_product_page.clear_quantity_field()
        first_product_page.add_amount_of_products_in_quantity_field(self.samsung_product_amount)
        first_product_page.click_on_add_to_cart_button()
        second_product_page.open()
        second_product_page.click_on_add_to_cart_button()
        shopping_cart_page.open_checkout_cart_url()
        actual_total_cost: Decimal = shopping_cart_page.get_total_sum_in_shopping_cart()
        actual_first_product_name_text: str = shopping_cart_page.get_first_product_name()
        actual_second_product_name_text: str = shopping_cart_page.get_second_product_name()
        self.assertEqual((actual_total_cost, actual_first_product_name_text, actual_second_product_name_text),
                         (self.expected_total_cost, self.expected_first_product_name,
                          self.expected_second_product_name))

    def test_removing_products_from_shopping_cart(self):
        """Тест на удаление товаров из корзины"""
        first_product_page = ProductPage(self.driver, self.first_product_id)
        second_product_page = ProductPage(self.driver, self.second_product_id)
        shopping_cart_page = ShoppingCart(self.driver)
        first_product_page.open()
        first_product_page.clear_quantity_field()
        first_product_page.add_amount_of_products_in_quantity_field(self.samsung_product_amount)
        first_product_page.click_on_add_to_cart_button()
        second_product_page.open()
        second_product_page.click_on_add_to_cart_button()
        shopping_cart_page.open_checkout_cart_url()
        shopping_cart_page.click_on_remove_buttons()
        actual_result = shopping_cart_page.get_text_for_empty_shopping_cart()
        expected_result = self.text_for_empty_shopping_cart
        self.assertEqual(actual_result, expected_result)
