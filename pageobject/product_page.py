from decimal import Decimal

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from pageobject.base_page import BasePage
from product_info_model import ProductInfo

from selenium.webdriver.support import expected_conditions as EC


class ProductPageLocator:
    CONTENT_WITH_PRODUCT_INFO = By.XPATH, '//div[@id="content"]//div[@class="col-sm-4"]'
    PRODUCT_NAME = By.TAG_NAME, 'h1'
    PRODUCT_BRAND = By.XPATH, '//div[@id="content"]//div[@class="col-sm-4"]//ul//a'
    PRODUCT_CODE_RAW_DATA = By.XPATH, '//li[contains(text(), "Product")]'
    RAW_DATA_WITH_PRICE = By.XPATH, '//ul[@class="list-unstyled"]//h2'
    RAW_DESCRIPTION_DATA = By.ID, 'tab-description'
    ADD_TO_CART_BUTTON = By.ID, 'button-cart'
    ELEMENT_WITH_FIRST_PARAGRAPH_TEXT = By.CSS_SELECTOR, '[face=Helvetica]'
    REVIEWS_TAB = By.CSS_SELECTOR, 'a[href="#tab-review"]'
    CONTINUE_BUTTON = By.ID, 'button-review'
    NOTIFICATION_ELEMENT = By.CSS_SELECTOR, 'div.alert.alert-dismissible'
    YOUR_NAME_FIELD = By.ID, 'input-name'
    YOUR_REVIEW_FIELD = By.ID, 'input-review'
    REVIEW_INFO = By.ID, 'review'
    COMPARISON_LINK = By.LINK_TEXT, 'product comparison'
    COMPARE_THIS_PRODUCT_BUTTON = By.CSS_SELECTOR, '[data-original-title="Compare this Product"]'


class ProductPage(BasePage):
    """Создаём отдельный page object для страницы продукта"""

    def __init__(self, driver: WebDriver, product_id: str) -> None:
        super().__init__(driver)
        self.product_id = product_id
        self.product_base_url_text: str = 'http://54.183.112.233/index.php?route=prod%20uct/%20product&product_id='

    def get_url(self) -> str:
        return f'{self.product_base_url_text}{self.product_id}'

    def get_product_info(self) -> ProductInfo:
        """Получение различных данных о товаре и формирование элемента класса ProductInfo с необходимыми аттрибутами"""

        content_with_product_info: WebElement = self.driver.find_element(*ProductPageLocator.CONTENT_WITH_PRODUCT_INFO)

        product_name: str = content_with_product_info.find_element(*ProductPageLocator.PRODUCT_NAME).text

        product_brand: str = content_with_product_info.find_element(*ProductPageLocator.PRODUCT_BRAND).text

        product_code: str = content_with_product_info.find_element(
            *ProductPageLocator.PRODUCT_CODE_RAW_DATA).text.replace('Product Code: ', '')

        product_price: str = content_with_product_info.find_element(
            *ProductPageLocator.RAW_DATA_WITH_PRICE).text.strip('$')

        actual_product = ProductInfo(name=product_name, price=Decimal(product_price),
                                     brand=product_brand, code=product_code)

        return actual_product

    def get_reviews_tab(self) -> WebElement:
        reviews_tab: WebElement = self.driver.find_element(*ProductPageLocator.REVIEWS_TAB)
        return reviews_tab

    def get_continue_button(self) -> WebElement:
        continue_button: WebElement = self.driver.find_element(*ProductPageLocator.CONTINUE_BUTTON)
        return continue_button

    def get_warning_notification_element_danger(self) -> WebElement:
        warning_notification: WebElement = self.driver.find_element(*ProductPageLocator.NOTIFICATION_ELEMENT)
        return warning_notification

    def get_message_about_success_review_sending(self) -> WebElement:
        warning_notification: WebElement = self.driver.find_element(*ProductPageLocator.NOTIFICATION_ELEMENT)
        return warning_notification

    def get_warning_notification_text(self) -> str:
        warning_notification = self.get_warning_notification_element_danger()
        return warning_notification.text

    def get_message_about_success_review_text(self) -> str:
        success_review_sending_notification = self.get_message_about_success_review_sending()
        return success_review_sending_notification.text

    def get_radiobutton_rating(self, value: str) -> WebElement:
        radio_button_selector = f'input[type="radio"][name="rating"][value="{value}"]'
        radio_button = self.driver.find_element(By.CSS_SELECTOR, radio_button_selector)
        return radio_button

    def get_your_name_field(self) -> WebElement:
        your_name = self.driver.find_element(*ProductPageLocator.YOUR_NAME_FIELD)
        return your_name

    def get_your_review_field(self) -> WebElement:
        your_review_field = self.driver.find_element(*ProductPageLocator.YOUR_REVIEW_FIELD)
        return your_review_field

    def get_compare_this_product_button(self) -> WebElement:
        compare_this_product_button: WebElement = self.driver.find_element(
            *ProductPageLocator.COMPARE_THIS_PRODUCT_BUTTON)
        return compare_this_product_button

    def get_comparison_adding_success_message(self) -> str:
        comparison_adding_success_message: WebElement = self.driver.find_element(
            *ProductPageLocator.NOTIFICATION_ELEMENT)
        return comparison_adding_success_message.text

    def get_product_comparison_link(self) -> WebElement:
        product_comparison_link = self.driver.find_element(*ProductPageLocator.COMPARISON_LINK)
        return product_comparison_link

    def get_quantity_field(self) -> WebElement:
        quantity_field = self.driver.find_element(By.ID, 'input-quantity')
        return quantity_field

    def add_amount_of_products_in_quantity_field(self, amount: int) -> None:
        self.get_quantity_field().send_keys(amount)

    def get_add_to_cart_button(self) -> WebElement:
        add_to_cart_button: WebElement = self.driver.find_element(By.ID, 'button-cart')
        return add_to_cart_button

    def get_success_message_about_adding_product_into_shopping_cart_text(self) -> str:
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.visibility_of_element_located(
            ProductPageLocator.NOTIFICATION_ELEMENT))
        success_message_element: WebElement = self.driver.find_element(
            *ProductPageLocator.NOTIFICATION_ELEMENT)

        return success_message_element.text.strip('\n×')

    def get_product_description(self) -> str:
        """Получение первого параграфа описания товара"""
        raw_description_data: WebElement = self.driver.find_element(*ProductPageLocator.RAW_DESCRIPTION_DATA)

        element_with_first_paragraph_text: str = raw_description_data.find_element(
            *ProductPageLocator.ELEMENT_WITH_FIRST_PARAGRAPH_TEXT).text

        return element_with_first_paragraph_text

    def clear_quantity_field(self) -> None:
        self.get_quantity_field().clear()

    def clear_your_review_field(self):
        self.get_your_review_field().clear()

    def enter_name_in_name_field(self, name: str) -> None:
        your_name_field = self.get_your_name_field()
        your_name_field.send_keys(name)
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.text_to_be_present_in_element_attribute(
            ProductPageLocator.YOUR_NAME_FIELD, 'value', name))

    def enter_text_in_your_review_field(self, text: str) -> None:
        your_review_field = self.get_your_review_field()
        your_review_field.send_keys(text)
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.text_to_be_present_in_element_attribute(
            ProductPageLocator.YOUR_REVIEW_FIELD, 'value', text))

    def click_on_continue_button(self):
        self.get_continue_button().click()
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.any_of(
            EC.visibility_of_element_located(ProductPageLocator.NOTIFICATION_ELEMENT),
            EC.visibility_of_element_located(ProductPageLocator.NOTIFICATION_ELEMENT)))

    def click_on_reviews_tab(self) -> None:
        reviews_tab = self.get_reviews_tab()
        reviews_tab.click()
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.presence_of_element_located(ProductPageLocator.REVIEW_INFO))

    def click_by_rating_radiobutton(self, rating: str):
        selected_radio_button: WebElement = self.driver.find_element(
            By.XPATH, f'//div[@class="col-sm-12"]//input[@type="radio" and @value={rating}]')
        initial_radio_button_state = selected_radio_button.is_selected()
        self.get_radiobutton_rating(rating).click()
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(lambda driver: selected_radio_button.is_selected() != initial_radio_button_state)

    def click_on_compare_this_product_button(self) -> None:
        self.get_compare_this_product_button().click()
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.visibility_of_element_located(ProductPageLocator.NOTIFICATION_ELEMENT))

    def click_on_product_comparison_link(self) -> None:
        self.get_product_comparison_link().click()
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.url_to_be('http://54.183.112.233/index.php?route=product/compare'))

    def click_on_add_to_cart_button(self) -> None:
        self.get_add_to_cart_button().click()
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.visibility_of_element_located(
            ProductPageLocator.ADD_TO_CART_BUTTON))
