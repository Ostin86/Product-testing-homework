from typing import List

from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, \
    visibility_of_all_elements_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageobject.base_page import BasePage


class ComparePage(BasePage):

    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=product/compare'

    def open_product_to_comparison_page(self, url):
        self.driver.get(url)

    def get_compare_this_product_button(self) -> WebElement:
        compare_this_product_button: WebElement = self.driver.find_element(By.CSS_SELECTOR,
                                                                           '[data-original-title="Compare this Product"]')
        return compare_this_product_button

    def get_product_comparison_link(self) -> WebElement:
        product_comparison_link = self.driver.find_element(By.LINK_TEXT, 'product comparison')
        return product_comparison_link

    def wait_comparison_adding_success_message(self) -> None:
        locator = By.CSS_SELECTOR, 'div.alert.alert-success.alert-dismissible'
        WebDriverWait(self.driver, timeout=5).until(visibility_of_element_located(locator))

    def wait_for_compare_this_product_button(self) -> None:
        locator = By.CSS_SELECTOR, '[data-original-title="Compare this Product"]'
        WebDriverWait(self.driver, timeout=5).until(visibility_of_element_located(locator))

    def wait_for_comparison_button(self) -> None:
        locator = By.LINK_TEXT, 'product comparison'
        WebDriverWait(self.driver, timeout=5).until(visibility_of_element_located(locator))

    def get_comparison_adding_success_message(self) -> str:
        comparison_adding_success_message: WebElement = self.driver.find_element(By.CSS_SELECTOR,
                                                                                 'div.alert.alert-success.alert-dismissible')
        return comparison_adding_success_message.text

    def get_added_to_comparison_products(self) -> List[WebElement]:
        added_to_comparison_products = self.driver.find_elements(By.CSS_SELECTOR,
                                                                     ' .table.table-bordered tbody a strong ')
        return added_to_comparison_products

    def wait_for_info_about_comparison_products(self) -> None:
        selector = '.table.table-bordered tbody a strong'
        elements_with_info_products: list[WebElement] = self.driver.find_elements(By.CSS_SELECTOR, selector)
        while len(elements_with_info_products) != 2:
            elements_with_info_products: list[WebElement] = self.driver.find_elements(By.CSS_SELECTOR, selector)

    def get_remove_buttons(self) -> List[WebElement]:
        remove_buttons_list: List[WebElement] = self.driver.find_elements(By.PARTIAL_LINK_TEXT, 'Remove')
        return remove_buttons_list

    def get_text_when_no_one_elements_in_comparison_list(self) -> str:
        no_one_elements_in_comparison_list: WebElement = self.driver.find_element(By.CSS_SELECTOR, 'div#content p')
        return no_one_elements_in_comparison_list.text

    def click_on_remove_buttons(self) -> None:
        elements: List[WebElement] = self.get_remove_buttons()
        while len(elements) > 0:
            try:
                elements[-1].click()
            except StaleElementReferenceException:
                elements: List[WebElement] = self.get_remove_buttons()

    def click_on_compare_this_product_button(self) -> None:
        self.get_compare_this_product_button().click()

    def click_on_product_comparison_link(self) -> None:
        self.get_product_comparison_link().click()
