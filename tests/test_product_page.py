import unittest
from decimal import Decimal

from pageobject.product_page import ProductPage
from webdriver_factory import WebDriverFactory
from product_info_model import ProductInfo


class ProductPageTests(unittest.TestCase):
    driver = None
    test_product_id: str = '42'
    text_description: str = 'The 30-inch Apple Cinema HD Display delivers'
    expected_product = ProductInfo(name='Apple Cinema 30"', price=Decimal(110),
                                   brand='Apple', code='Product 15')

    @classmethod
    def setUpClass(cls) -> None:
        """Предустановка. Выполняется один раз перед всеми тестами"""
        cls.driver = WebDriverFactory.get_driver()
        cls.product_page = ProductPage(cls.driver, cls.test_product_id)

    def setUp(self) -> None:
        """Действия до теста"""
        self.product_page.open()

    @classmethod
    def tearDownClass(cls):
        """Действия после теста"""
        cls.driver.quit()

    def test_getting_product_info(self):
        """Тест для проверки наличия необходимой информации о продукте"""
        actual_product = self.product_page.get_product_info()
        self.assertEqual(self.expected_product, actual_product)

    def test_getting_description(self):
        """Тест для проверки наличия описания продукта"""
        actual_description_text = self.product_page.get_product_description()
        expected_part_of_text_description: str = self.text_description
        self.assertTrue(expected_part_of_text_description in actual_description_text)
