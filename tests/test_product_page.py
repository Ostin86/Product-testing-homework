import unittest
from decimal import Decimal

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pageobject.product_page import ProductPage
from webdriver_factory import WebDriverFactory


class ProductPageTests(unittest.TestCase):
    test_product_id: str = '42'
    product_name: str = 'Apple Cinema 30"'
    product_brand: str = 'Apple'
    product_code: str = 'Product Code: Product 15'
    text_description: str = 'The 30-inch Apple Cinema HD Display delivers'

    def setUp(self) -> None:
        """Действия до теста"""
        self.driver = self.driver = WebDriverFactory.get_driver()
        self.product_page = ProductPage(self.driver, self.test_product_id)
        self.product_page.open()

    def tearDown(self):
        """Действия после теста"""
        self.driver.close()

    def test_getting_product_info(self):
        """Тест для проверки наличия необходимой информации о продукте"""
        expected_product_name: str = self.product_name
        expected_product_brand: str = self.product_brand
        expected_product_code_raw_data: str = self.product_code
        expected_cost: Decimal = Decimal(110)

        expected_product_info: list = [expected_product_name, expected_product_brand,
                                       expected_product_code_raw_data, expected_cost]

        actual_product_name = self.product_page.get_product_info()[0]
        actual_product_brand = self.product_page.get_product_info()[1]
        actual_product_code = self.product_page.get_product_info()[2][1]
        actual_cost = Decimal(self.product_page.get_product_info()[3].strip('$'))

        actual_product_info: list = [actual_product_name, actual_product_brand, actual_product_code,
                                     actual_cost]

        self.assertEqual(expected_product_info, actual_product_info)

    def test_getting_description(self):
        """Тест для проверки наличия описания продукта"""
        actual_description_text = self.product_page.get_product_description()
        expected_part_of_text_description: str = self.text_description
        self.assertTrue(expected_part_of_text_description in actual_description_text)
