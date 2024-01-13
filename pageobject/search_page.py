from dataclasses import dataclass
from decimal import Decimal
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageobject.base_page import BasePage
from product_info_model import ProductInfo
from extract_price_func import extract_decimal_price


class SearchPageLocator:
    SEARCH_FIELD = By.CLASS_NAME, 'input-lg'
    SEARCH_CRITERIA_FIELD = By.ID, 'input-search'
    PRODUCT_NAME_FIELD = By.TAG_NAME, 'h4'
    SEARCH_IN_PRODUCT_DESCTIPTION_CHECKBOX = By.ID, 'description'
    FIND_BUTTON = By.CLASS_NAME, 'btn-default'
    SEARCH_BUTTON = By.ID, 'button-search'
    TEXT_ABOUT_PR0DUCT_THAT_DOESNT_EXIST = By.XPATH, ('//h2[text()="Products meeting the search '
                                                      'criteria"]/following-sibling::p')
    SEARCH_RESULTS = By.CLASS_NAME, 'product-layout'
    PRICE = By.CLASS_NAME, 'price'


class SearchPage(BasePage):

    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=prod%20uct/search'

    def get_search_field(self) -> WebElement:
        search_field: WebElement = self.driver.find_element(*SearchPageLocator.SEARCH_FIELD)
        return search_field

    def get_search_criteria_field(self) -> WebElement:
        search_criteria_field: WebElement = self.driver.find_element(*SearchPageLocator.SEARCH_CRITERIA_FIELD)
        return search_criteria_field

    def get_product_name(self) -> str:
        product_name: str = self.driver.find_element(*SearchPageLocator.PRODUCT_NAME_FIELD).text
        return product_name

    def get_product_description_checkbox_search(self) -> WebElement:
        search_in_product_description_checkbox = self.driver.find_element(
            *SearchPageLocator.SEARCH_IN_PRODUCT_DESCTIPTION_CHECKBOX)
        return search_in_product_description_checkbox

    def get_find_button(self) -> WebElement:
        find_button = self.driver.find_element(*SearchPageLocator.FIND_BUTTON)
        return find_button

    def get_search_button(self) -> WebElement:
        search_button = self.driver.find_element(*SearchPageLocator.SEARCH_BUTTON)
        return search_button

    def get_product_that_doesnt_exist_text(self) -> str:
        text_about_product_that_doesnt_exist = self.driver.find_element(
            *SearchPageLocator.TEXT_ABOUT_PR0DUCT_THAT_DOESNT_EXIST)
        return text_about_product_that_doesnt_exist.text

    def get_search_results(self) -> List[ProductInfo]:
        """Метод, который возвращает список имен и цен для найденных продуктов"""
        product_tags = self.driver.find_elements(*SearchPageLocator.SEARCH_RESULTS)
        products: List[ProductInfo] = []

        for product_div_tag in product_tags:
            name: str = product_div_tag.find_element(*SearchPageLocator.PRODUCT_NAME_FIELD).text
            price_text: str = product_div_tag.find_element(*SearchPageLocator.PRICE).text
            product = ProductInfo(
                name=name,
                price=Decimal(extract_decimal_price(price_text))
            )
            products.append(product)
        return products

    def get_search_result_names(self) -> List[str]:
        search_results = self.get_search_results()
        search_result_names: list[str] = []
        for search_result in search_results:
            search_result_name = search_result.name
            search_result_names.append(search_result_name)
        return search_result_names

    def clear_search_field(self) -> None:
        search_field = self.get_search_field()
        search_field.clear()

    def clear_search_criteria_field(self) -> None:
        search_criteria_field = self.get_search_criteria_field()
        search_criteria_field.clear()

    def enter_search_request_in_search_field(self, request: str) -> None:
        search_field: WebElement = self.get_search_field()
        search_field.send_keys(request)

    def enter_search_request_in_search_criteria_field(self, request: str) -> None:
        search_criteria_field: WebElement = self.get_search_criteria_field()
        search_criteria_field.send_keys(request)

    def click_by_search_in_product_description_checkbox(self) -> None:
        search_in_product_description_checkbox = self.get_product_description_checkbox_search()
        search_in_product_description_checkbox.click()

    def click_by_find_button(self) -> None:
        find_button = self.get_find_button()
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.element_to_be_clickable(SearchPageLocator.FIND_BUTTON))
        find_button.click()

    def click_by_search_button(self) -> None:
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.element_to_be_clickable(SearchPageLocator.SEARCH_BUTTON))
        self.get_search_button().click()
