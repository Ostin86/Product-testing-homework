from dataclasses import dataclass
from decimal import Decimal
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pageobject.base_page import BasePage


def extract_decimal_price(text: str) -> Decimal:
    """Функция, которая извлекает из строки цену"""

    split_by_lines: List[str] = text.split("\n")
    first_price_lines = split_by_lines[0].split(' ')
    first_price = first_price_lines[0][1:]
    first_price_without_punctuation = first_price.replace(",", "")

    return Decimal(first_price_without_punctuation)


@dataclass
class ProductInfo:
    name: str
    price: Decimal


class SearchPage(BasePage):

    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=prod%20uct/search'

    def get_search_field(self) -> WebElement:
        search_field: WebElement = self.driver.find_element(By.CLASS_NAME, 'input-lg')
        return search_field

    def get_search_criteria_field(self) -> WebElement:
        search_criteria_field: WebElement = self.driver.find_element(By.ID, 'input-search')
        return search_criteria_field

    def get_product_name(self) -> str:
        product_name: str = self.driver.find_element(By.TAG_NAME, 'h4').text
        return product_name

    def get_search_in_product_description_checkbox(self) -> WebElement:
        search_in_product_description_checkbox = self.driver.find_element(By.ID, 'description')
        return search_in_product_description_checkbox

    def get_find_button(self) -> WebElement:
        find_button = self.driver.find_element(By.CLASS_NAME, 'btn-default')
        return find_button

    def get_search_button(self) -> WebElement:
        search_button = self.driver.find_element(By.ID, 'button-search')
        return search_button

    def get_text_about_product_that_doesnt_exist(self) -> str:
        text_about_product_that_doesnt_exist = self.driver.find_element(By.XPATH,
                                                                        '//h2[text()="Products meeting the search '
                                                                        'criteria"]/following-sibling::p')
        return text_about_product_that_doesnt_exist.text

    def get_search_results(self) -> List[ProductInfo]:
        """Метод, который возвращает список имен и цен для найденных продуктов"""
        product_tags = self.driver.find_elements(By.CLASS_NAME, 'product-layout')
        products: List[ProductInfo] = []

        for product_div_tag in product_tags:
            name: str = product_div_tag.find_element(By.TAG_NAME, 'h4').text
            price_text: str = product_div_tag.find_element(By.CLASS_NAME, 'price').text
            product = ProductInfo(
                name=name,
                price=Decimal(extract_decimal_price(price_text))
            )
            products.append(product)
        return products

    def clear_search_field(self) -> None:
        search_field = self.get_search_field()
        search_field.clear()

    def clear_search_criteria_field(self) -> None:
        search_criteria_field = self.get_search_criteria_field()
        search_criteria_field.clear()

    def enter_search_request_in_search_field(self, request: str | int) -> None:
        search_field: WebElement = self.get_search_field()
        search_field.send_keys(request)

    def enter_search_request_in_search_criteria_field(self, request: str | int) -> None:
        search_criteria_field: WebElement = self.get_search_criteria_field()
        search_criteria_field.send_keys(request)

    def click_by_search_in_product_description_checkbox(self) -> None:
        search_in_product_description_checkbox = self.get_search_in_product_description_checkbox()
        search_in_product_description_checkbox.click()

    def click_by_find_button(self) -> None:
        find_button = self.get_find_button()
        find_button.click()

    def click_by_search_button(self) -> None:
        self.get_search_button().click()
