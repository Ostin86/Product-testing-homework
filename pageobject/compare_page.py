from typing import List

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pageobject.base_page import BasePage


class ComparePageLocator:
    ADDED_TO_COMPARISON_BUTTON = By.CSS_SELECTOR, ' .table.table-bordered tbody a strong '
    REMOVE_BUTTON = By.PARTIAL_LINK_TEXT, 'Remove'
    TEXT_WHEN_NO_ELEMENTS_ARE_IN_COMPARISON_LIST = By.CSS_SELECTOR, 'div#content p'


class ComparePage(BasePage):

    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=product/compare'

    def open_product_to_comparison_page(self, url):
        self.driver.get(url)

    def get_added_to_comparison_products(self) -> List[WebElement]:
        added_to_comparison_products = self.driver.find_elements(*ComparePageLocator.ADDED_TO_COMPARISON_BUTTON)
        return added_to_comparison_products

    def get_remove_buttons(self) -> List[WebElement]:
        remove_buttons_list: List[WebElement] = self.driver.find_elements(*ComparePageLocator.REMOVE_BUTTON)
        return remove_buttons_list

    def get_text_when_no_one_elements_in_comparison_list(self) -> str:
        no_one_elements_in_comparison_list: WebElement = self.driver.find_element(
            *ComparePageLocator.TEXT_WHEN_NO_ELEMENTS_ARE_IN_COMPARISON_LIST)
        return no_one_elements_in_comparison_list.text

    def click_on_remove_buttons(self) -> None:
        elements: List[WebElement] = self.get_remove_buttons()
        while len(elements) > 0:
            try:
                elements[-1].click()
            except StaleElementReferenceException:
                elements: List[WebElement] = self.get_remove_buttons()
