from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from pageobject.base_page import BasePage

from selenium.webdriver.support import expected_conditions as EC


class ProductPageLocator:
    CONTENT_WITH_PRODUCT_INFO = By.ID, 'content'
    PRODUCT_NAME = By.TAG_NAME, 'h1'
    PRODUCT_BRAND = By.CSS_SELECTOR, '.list-unstyled li a'
    PRODUCT_CODE_RAW_DATA = By.CLASS_NAME, 'list-unstyled'
    RAW_DATA_WITH_PRICE = By.TAG_NAME, 'h2'
    RAW_DESCRIPTION_DATA = By.ID, 'tab-description'
    ELEMENT_WITH_FIRST_PARAGRAPH_TEXT = By.CSS_SELECTOR, '[face=Helvetica]'
    REVIEWS_TAB = By.CSS_SELECTOR, 'a[href="#tab-review"]'
    CONTINUE_BUTTON = By.ID, 'button-review'
    WARNING_NOTIFICATION_ELEMENT = By.CSS_SELECTOR, 'div.alert.alert-danger.alert-dismissible'
    SUCCESS_REVIEW_SENDING = By.CSS_SELECTOR, 'div.alert.alert-success.alert-dismissible'
    RADIO_BUTTON_RATING_BY_DEFAULT = 5
    RADIO_BUTTON = By.CSS_SELECTOR, f'input[type="radio"][name="rating"][value="{RADIO_BUTTON_RATING_BY_DEFAULT}"]'
    YOUR_NAME_FIELD = By.ID, 'input-name'
    YOUR_REVIEW_FIELD = By.ID, 'input-review'
    TEXT_FOR_WARNING_ABOUT_PRODUCT_ABSENCE = By.CSS_SELECTOR, 'div.alert.alert-danger.alert-dismissible'
    WAIT_FOR_TEXT_OF_SUCCESS_REVIEW_SENDING = By.CSS_SELECTOR, 'div.alert.alert-success.alert-dismissible'
    REVIEW_INFO = By.ID, 'review'
    COMPARISON_LINK = By.LINK_TEXT, 'product comparison'
    COMPARE_THIS_PRODUCT_BUTTON = By.CSS_SELECTOR, '[data-original-title="Compare this Product"]'
    COMPARISON_ADDING_SUCCESS_MESSAGE = By.CSS_SELECTOR, 'div.alert.alert-success.alert-dismissible'
    SUCCESS_MESSAGE_AFTER_ADDING_PRODUCT_INTO_SHOPPING_CART = By.CSS_SELECTOR, ('#product-product > '
                                                                                  'div.alert.alert-success.alert'
                                                                                  '-dismissible')


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
        content_with_product_info: WebElement = self.driver.find_element(*ProductPageLocator.CONTENT_WITH_PRODUCT_INFO)

        product_name_text: str = content_with_product_info.find_element(*ProductPageLocator.PRODUCT_NAME).text

        product_brand: str = content_with_product_info.find_element(*ProductPageLocator.PRODUCT_BRAND).text

        product_code_raw_data: list = content_with_product_info.find_element(
            *ProductPageLocator.PRODUCT_CODE_RAW_DATA).text.split('\n')

        raw_data_with_price: str = content_with_product_info.find_elements(
            *ProductPageLocator.RAW_DATA_WITH_PRICE)[1].text

        return product_name_text, product_brand, product_code_raw_data, raw_data_with_price

    def get_product_description(self) -> str:
        """Получение первого параграфа описания товара"""
        raw_description_data: WebElement = self.driver.find_element(*ProductPageLocator.RAW_DESCRIPTION_DATA)

        element_with_first_paragraph_text: str = raw_description_data.find_element(
            *ProductPageLocator.ELEMENT_WITH_FIRST_PARAGRAPH_TEXT).text

        return element_with_first_paragraph_text

    def get_reviews_tab(self) -> WebElement:
        reviews_tab: WebElement = self.driver.find_element(*ProductPageLocator.REVIEWS_TAB)
        return reviews_tab

    def get_continue_button(self) -> WebElement:
        continue_button: WebElement = self.driver.find_element(*ProductPageLocator.CONTINUE_BUTTON)
        return continue_button

    def get_warning_notification_element_danger(self) -> WebElement:
        warning_notification: WebElement = self.driver.find_element(*ProductPageLocator.WARNING_NOTIFICATION_ELEMENT)
        return warning_notification

    def get_message_about_success_review_sending(self) -> WebElement:
        warning_notification: WebElement = self.driver.find_element(*ProductPageLocator.SUCCESS_REVIEW_SENDING)
        return warning_notification

    def get_warning_notification_text(self) -> str:
        warning_notification = self.get_warning_notification_element_danger()
        return warning_notification.text

    def get_message_about_success_review_text(self) -> str:
        success_review_sending_notification = self.get_message_about_success_review_sending()
        return success_review_sending_notification.text

    def get_rating_radiobutton(self, value: int) -> WebElement:
        radio_button = self.driver.find_element(*ProductPageLocator.RADIO_BUTTON)
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
            *ProductPageLocator.COMPARISON_ADDING_SUCCESS_MESSAGE)
        return comparison_adding_success_message.text

    def get_product_comparison_link(self) -> WebElement:
        product_comparison_link = self.driver.find_element(*ProductPageLocator.COMPARISON_LINK)
        try:
            wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
            wait.until(EC.visibility_of_element_located(ProductPageLocator.COMPARISON_LINK))
        except TimeoutException:
            print(f"Кнопка сравнения товаров не найдена!")
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
        success_message_element: WebElement = self.driver.find_element(
            *ProductPageLocator.SUCCESS_MESSAGE_AFTER_ADDING_PRODUCT_INTO_SHOPPING_CART)
        return success_message_element.text

    def clear_quantity_field(self) -> None:
        self.get_quantity_field().clear()

    def clear_your_name_field(self) -> None:
        self.get_your_name_field().clear()

    def clear_your_review_field(self):
        self.get_your_review_field().clear()

    def enter_name_in_name_field(self, name: str) -> None:
        your_name_field = self.get_your_name_field()
        your_name_field.send_keys(name)
        try:
            wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
            wait.until(EC.text_to_be_present_in_element_attribute(
                ProductPageLocator.YOUR_NAME_FIELD, 'value', name))
        except TimeoutException:
            print(f"Текст '{name}' не появился в поле за отведенное время")

    def enter_text_in_your_review_field(self, text: str) -> None:
        your_review_field = self.get_your_review_field()
        your_review_field.send_keys(text)
        try:
            wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
            wait.until(EC.text_to_be_present_in_element_attribute(
                ProductPageLocator.YOUR_REVIEW_FIELD, 'value', text))
        except TimeoutException:
            print(f"Текст '{text}' не появился в поле за отведенное время")

    def click_on_continue_button(self):
        self.get_continue_button().click()
        self.wait_text_of_sending_review_status()

    def click_on_reviews_tab(self) -> None:
        reviews_tab = self.get_reviews_tab()
        reviews_tab.click()
        try:
            wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
            wait.until(EC.presence_of_element_located(ProductPageLocator.REVIEW_INFO))
        except TimeoutException:
            print(f"Элемент 'Review info' не появился в поле за отведенное время")

    def click_by_rating_radiobutton(self):
        self.get_rating_radiobutton(ProductPageLocator.RADIO_BUTTON_RATING_BY_DEFAULT).click()
        try:
            wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
            wait.until(EC.text_to_be_present_in_element_attribute(
                ProductPageLocator.RADIO_BUTTON, 'value', str(ProductPageLocator.RADIO_BUTTON_RATING_BY_DEFAULT)))
        except TimeoutException:
            print(f"Ошибка в установке значения рейтинга товара!")

    def click_on_compare_this_product_button(self) -> None:
        self.get_compare_this_product_button().click()
        try:
            wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
            wait.until(EC.visibility_of_element_located(ProductPageLocator.WAIT_FOR_TEXT_OF_SUCCESS_REVIEW_SENDING))
        except TimeoutException:
            print(f"Кнопка добавления товара в список сравнения товаров не найдена!")

    def click_on_product_comparison_link(self) -> None:
        self.get_product_comparison_link().click()

    def click_on_add_to_cart_button(self) -> None:
        self.get_add_to_cart_button().click()
        try:
            wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
            wait.until(EC.visibility_of_element_located(
                ProductPageLocator.SUCCESS_MESSAGE_AFTER_ADDING_PRODUCT_INTO_SHOPPING_CART))
        except TimeoutException:
            print(f"Сообщение об успешном добавлении товара в список сравнения не найдено!")

    def wait_text_of_sending_review_status(self) -> None:
        wait = WebDriverWait(self.driver, BasePage.TIME_OUT)
        wait.until(EC.any_of(
            EC.visibility_of_element_located(ProductPageLocator.TEXT_FOR_WARNING_ABOUT_PRODUCT_ABSENCE),
            EC.visibility_of_element_located(ProductPageLocator.WAIT_FOR_TEXT_OF_SUCCESS_REVIEW_SENDING)))
