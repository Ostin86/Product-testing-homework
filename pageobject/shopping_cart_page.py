from decimal import Decimal
from typing import List

from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import invisibility_of_element, text_to_be_present_in_element, \
    invisibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageobject.base_page import BasePage


class ShoppingCartLocator:
    PRODUCT_NAMES = By.CSS_SELECTOR, '.table-responsive table tbody tr .text-left a'
    REMOVE_BUTTON = By.CSS_SELECTOR, '[data-original-title="Remove"]'
    ELEMENT_WITH_INFO_IF_SHOPPING_CART_IS_EMPTY = By.CSS_SELECTOR, 'div#content p'
    ELEMENT_WITH_TOTAL_SUM_IN_SHOPPING_CART = By.CSS_SELECTOR, '.col-sm-4.col-sm-offset-8 table.table-bordered'


class ShoppingCart(BasePage):

    def get_total_sum_in_shopping_cart(self) -> Decimal:
        cost_info: list = self.get_element_with_total_sum_in_shopping_cart().text.split('\n')
        total_str_value: str = cost_info[-1].strip('Total: $')
        total_int_value: Decimal = Decimal(total_str_value)
        return total_int_value

    def get_url(self):
        return 'http://54.183.112.233/index.php?route=checkout/cart'

    def open_checkout_cart_url(self) -> None:
        self.driver.get(self.get_url())

    def get_all_product_names_from_shopping_cart(self) -> List[WebElement]:
        product_names: List[WebElement] = self.driver.find_elements(*ShoppingCartLocator.PRODUCT_NAMES)
        return product_names

    def get__product_names_in_shopping_cart(self) -> list[str]:
        product_names: list = []
        for element in self.get_all_product_names_from_shopping_cart():
            product_names.append(element.text)
        return product_names

    def get_remove_buttons_list(self) -> List[WebElement]:
        remove_buttons: List[WebElement] = self.driver.find_elements(*ShoppingCartLocator.REMOVE_BUTTON)
        return remove_buttons

    def get_empty_shopping_cart_text(self) -> str:
        text_for_empty_shopping_cart: str = self.driver.find_element(
            *ShoppingCartLocator.ELEMENT_WITH_INFO_IF_SHOPPING_CART_IS_EMPTY).text
        return text_for_empty_shopping_cart

    def get_element_with_total_sum_in_shopping_cart(self) -> WebElement:
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.visibility_of_element_located(ShoppingCartLocator.ELEMENT_WITH_TOTAL_SUM_IN_SHOPPING_CART))
        element_with_total_sum_in_shopping_cart: WebElement = self.driver.find_element(
            *ShoppingCartLocator.ELEMENT_WITH_TOTAL_SUM_IN_SHOPPING_CART)
        return element_with_total_sum_in_shopping_cart

    def click_on_remove_buttons(self) -> None:
        elements: List[WebElement] = self.get_remove_buttons_list()
        while len(elements) > 0:
            try:
                elements[-1].click()
            except StaleElementReferenceException:
                elements: List[WebElement] = self.get_remove_buttons_list()
