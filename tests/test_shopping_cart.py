import unittest
from decimal import Decimal

from pageobject.shopping_cart_page import ShoppingCart
from pageobject.product_page import ProductPage
from webdriver_factory import WebDriverFactory


class ShoppingCartTest(unittest.TestCase):
    driver = None
    first_product_id: str = '33'
    second_product_id: str = '47'
    initial_product_amount: int = 1
    samsung_product_amount: int = 2
    successful_adding_samsung_product_to_cart_message: str = (
        'Success: You have added Samsung SyncMaster 941BW to your '
        'shopping cart!')
    successful_adding_hp_product_to_cart_message: str = 'Success: You have added HP LP3065 to your shopping cart!'
    expected_total_cost: Decimal = Decimal('606.00')
    expected_product_names: list = ['Samsung SyncMaster 941BW', 'HP LP3065']
    text_for_empty_shopping_cart: str = 'Your shopping cart is empty!'

    @classmethod
    def setUpClass(cls) -> None:
        cls.driver = WebDriverFactory.get_driver()
        cls.first_product_page = ProductPage(cls.driver, cls.first_product_id)
        cls.second_product_page = ProductPage(cls.driver, cls.second_product_id)
        cls.shopping_cart_page = ShoppingCart(cls.driver)

    def setUp(self):
        """Действия до теста"""

    @classmethod
    def tearDownClass(cls):
        """Действия после теста"""
        cls.driver.quit()

    def test_adding_necessary_amount_product_into_cart(self):
        """Добавление необходимого количества одного из товаров в корзину"""
        self.first_product_page.open()
        self.first_product_page.clear_quantity_field()
        self.first_product_page.add_amount_of_products_in_quantity_field(self.samsung_product_amount)
        self.first_product_page.click_on_add_to_cart_button()
        actual_result: str = self.first_product_page.get_success_message_about_adding_product_into_shopping_cart_text()
        expected_result: str = self.successful_adding_samsung_product_to_cart_message
        self.assertEqual(expected_result, actual_result)

        """Добавление одного товара в корзину"""
        self.second_product_page.open()
        self.second_product_page.clear_quantity_field()
        self.second_product_page.add_amount_of_products_in_quantity_field(self.initial_product_amount)
        self.second_product_page.click_on_add_to_cart_button()
        actual_result: str = self.second_product_page.get_success_message_about_adding_product_into_shopping_cart_text()
        expected_result: str = self.successful_adding_hp_product_to_cart_message
        self.assertEqual(expected_result, actual_result)

        """Проверка общей стоимости товаров в корзине и её очистка"""
        self.shopping_cart_page.open()
        actual_total_cost: Decimal = self.shopping_cart_page.get_total_sum_in_shopping_cart()
        actual_product_names: list[str] = self.shopping_cart_page.get__product_names_in_shopping_cart()
        self.assertEqual(self.expected_total_cost, actual_total_cost)
        self.assertEqual(self.expected_product_names, actual_product_names)

        self.shopping_cart_page.clear_shopping_cart()
        expected_result = self.text_for_empty_shopping_cart
        actual_result = self.shopping_cart_page.get_empty_shopping_cart_text()
        self.assertEqual(expected_result, actual_result)
