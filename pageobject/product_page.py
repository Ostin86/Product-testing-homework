from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pageobject.base_page import BasePage


class ProductPage(BasePage):
    """Создаём отдельный page object для страницы продукта"""

    def __init__(self, driver: WebDriver, product_id: str) -> None:
        super().__init__(driver)
        self.product_id = product_id
        self.product_base_url_text: str = 'http://54.183.112.233/index.php?route=prod%20uct/%20product&product_id='

    def get_product_url(self) -> str:
        return f'{self.product_base_url_text}{self.product_id}'

    def open(self):
        """Метод для открытия страницы"""
        self.driver.get(self.get_product_url())

    def get_product_info(self) -> tuple:
        """Получение различных данных о товаре"""
        content_with_product_info: WebElement = self.driver.find_element(By.ID, 'content')
        product_name: str = content_with_product_info.find_element(By.TAG_NAME, 'h1').text
        product_brand: str = content_with_product_info.find_element(By.CSS_SELECTOR, '.list-unstyled li a').text
        product_code_raw_data: list = content_with_product_info.find_element(By.CLASS_NAME, 'list-unstyled').text.split(
            '\n')
        price_raw_data_price: str = content_with_product_info.find_elements(By.TAG_NAME, 'h2')[1].text
        return product_name, product_brand, product_code_raw_data, price_raw_data_price

    def get_product_description(self) -> str:
        """Получение первого параграфа описания товара"""
        raw_description_data: WebElement = self.driver.find_element(By.ID, 'tab-description')
        element_with_first_paragraph_text: str = raw_description_data.find_element(By.CSS_SELECTOR,
                                                                                   '[face=Helvetica]').text
        return element_with_first_paragraph_text
