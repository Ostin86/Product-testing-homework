from decimal import Decimal
from typing import List

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from pageobject.base_page import BasePage


class ShoppingCart(BasePage):

    def get_total_sum_in_shopping_cart(self) -> Decimal:
        cost_info: list = self.get_element_with_total_sum_in_shopping_cart().text.split('\n')
        total_str_value: str = cost_info[-1].strip('Total: $')
        total_int_value: Decimal = Decimal(total_str_value)
        return total_int_value

    def get_url(self):
        return 'http://54.183.112.233/index.php?route=checkout/cart'

    def open_product_to_cart_adding(self, url):
        self.driver.get(url)

    def get_quantity_field(self) -> WebElement:
        quantity_field = self.driver.find_element(By.ID, 'input-quantity')
        return quantity_field

    def clear_quantity_field(self) -> None:
        self.get_quantity_field().clear()

    def add_amount_of_products_in_quantity_field(self, amount: int) -> None:
        self.get_quantity_field().send_keys(amount)

    def get_add_to_cart_button(self) -> WebElement:
        add_to_cart_button: WebElement = self.driver.find_element(By.ID, 'button-cart')
        return add_to_cart_button

    def get_success_message_text(self) -> str:
        success_message_element: WebElement = self.driver.find_element(By.CSS_SELECTOR,
                                                                       '#product-product > div.alert.alert-success.alert-dismissible')
        return success_message_element.text

    def wait_comparison_adding_success_message(self) -> None:
        locator = By.CSS_SELECTOR, '#product-product > div.alert.alert-success.alert-dismissible'
        WebDriverWait(self.driver, timeout=5).until(visibility_of_element_located(locator))

    def click_on_add_to_cart_button(self) -> None:
        self.get_add_to_cart_button().click()

    def open_checkout_cart_url(self) -> None:
        self.driver.get(self.get_url())

    def get_product_names(self) -> List[WebElement]:
        product_names: List[WebElement] = self.driver.find_elements(By.CSS_SELECTOR, '.table-responsive table tbody tr .text-left a')
        return product_names

    def get_first_product_name(self) -> str:
        return self.get_product_names()[0].text

    def get_second_product_name(self) -> str:
        return self.get_product_names()[1].text

    def get_remove_buttons(self) -> List[WebElement]:
        remove_buttons: List[WebElement] = self.driver.find_elements(By.CSS_SELECTOR, '[data-original-title="Remove"]')
        return remove_buttons

    def get_text_for_empty_shopping_cart(self) -> str:
        text_for_empty_shopping_cart: str = self.driver.find_element(By.CSS_SELECTOR, 'div#content p').text
        return text_for_empty_shopping_cart

    def get_element_with_total_sum_in_shopping_cart(self) -> WebElement:
        element_with_total_sum_in_shopping_cart: WebElement = self.driver.find_element(By.CSS_SELECTOR,
                                                                                       '.col-sm-4.col-sm-offset-8 table.table-bordered')
        return element_with_total_sum_in_shopping_cart

    def click_on_remove_buttons(self) -> None:
        elements: List[WebElement] = self.get_remove_buttons()
        while len(elements) > 0:
            try:
                elements[-1].click()
            except StaleElementReferenceException:
                elements: List[WebElement] = self.get_remove_buttons()
