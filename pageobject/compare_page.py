from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from pageobject.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class ComparePageLocator:
    ADDED_TO_COMPARISON_BUTTON = By.CSS_SELECTOR, ' .table.table-bordered tbody a strong '
    REMOVE_BUTTON = By.PARTIAL_LINK_TEXT, 'Remove'
    TEXT_WHEN_NO_ELEMENTS_ARE_IN_COMPARISON_LIST = By.CSS_SELECTOR, 'div#content p'


class ComparePage(BasePage):

    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=product/compare'

    def get_added_to_comparison_products(self) -> List[WebElement]:
        added_to_comparison_products = self.driver.find_elements(*ComparePageLocator.ADDED_TO_COMPARISON_BUTTON)
        return added_to_comparison_products

    def get_added_to_comparison_products_names(self) -> List[str]:
        added_to_comparison_products = self.get_added_to_comparison_products()
        added_to_comparison_products_names: List[str] = [product.text for product in added_to_comparison_products]
        return added_to_comparison_products_names

    def get_remove_buttons_elements(self) -> List[WebElement]:
        remove_buttons_list: List[WebElement] = self.driver.find_elements(*ComparePageLocator.REMOVE_BUTTON)
        return remove_buttons_list

    def get_no_one_elements_in_comparison_list_text(self) -> str:
        no_one_elements_in_comparison_list: WebElement = self.driver.find_element(
            *ComparePageLocator.TEXT_WHEN_NO_ELEMENTS_ARE_IN_COMPARISON_LIST)
        return no_one_elements_in_comparison_list.text

    def get_product_remove_button(self, product_id: str) -> WebElement:
        product_remove_button: WebElement = self.driver.find_element(
            By.XPATH, f"//a[@class='btn btn-danger btn-block' and contains(@href, {product_id})]"
        )
        return product_remove_button

    def click_on_product_remove_button(self, product_remove_button: WebElement) -> None:
        product_remove_button.click()
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.invisibility_of_element(product_remove_button))

    def clear_comparison_list(self, product_ids: list[str]):
        for product_id in product_ids:
            product_remove_button: WebElement = self.get_product_remove_button(product_id)
            self.click_on_product_remove_button(product_remove_button)
