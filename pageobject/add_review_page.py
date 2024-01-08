from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageobject.base_page import BasePage


class AddReviewPage(BasePage):

    def get_url(self) -> str:
        return 'http://54.183.112.233/index.php?route=product/product&product_id=42'

    def get_reviews_tab(self) -> WebElement:
        reviews_tab: WebElement = self.driver.find_element(By.CSS_SELECTOR, 'a[href="#tab-review"]')
        return reviews_tab

    def get_continue_button(self) -> WebElement:
        continue_button: WebElement = self.driver.find_element(By.ID, 'button-review')
        return continue_button

    def get_warning_notification_element_danger(self) -> WebElement:
        warning_notification: WebElement = self.driver.find_element(By.CSS_SELECTOR, 'div.alert.alert-danger.alert'
                                                                                     '-dismissible')
        return warning_notification

    def get_message_about_success_review_sending(self) -> WebElement:
        warning_notification: WebElement = self.driver.find_element(By.CSS_SELECTOR, 'div.alert.alert-success.alert'
                                                                                     '-dismissible')
        return warning_notification

    def get_warning_notification_text(self) -> str:
        warning_notification = self.get_warning_notification_element_danger()
        return warning_notification.text

    def get_message_about_success_review_text(self) -> str:
        success_review_sending_notification = self.get_message_about_success_review_sending()
        return success_review_sending_notification.text

    def get_rating_radiobutton(self) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, 'input[type="radio"][name="rating"][value="4"]')

    def get_your_name_field(self) -> WebElement:
        your_name = self.driver.find_element(By.ID, 'input-name')
        return your_name

    def get_your_review_field(self) -> WebElement:
        your_review_field = self.driver.find_element(By.ID, 'input-review')
        return your_review_field

    def clear_your_name_field(self) -> None:
        self.get_your_name_field().clear()

    def clear_your_review_field(self):
        self.get_your_review_field().clear()

    def enter_name_in_name_field(self, name: str) -> None:
        your_name_field = self.get_your_name_field()
        your_name_field.send_keys(name)

    def enter_text_in_your_review_field(self, text: str) -> None:
        your_review_field = self.get_your_review_field()
        your_review_field.send_keys(text)

    def click_on_continue_button(self):
        self.get_continue_button().click()

    def click_on_reviews_tab(self) -> None:
        reviews_tab = self.get_reviews_tab()
        reviews_tab.click()

    def click_by_rating_radiobutton(self):
        self.get_rating_radiobutton().click()
        

    def wait_text_of_warning_presence(self) -> None:
        locator = By.CSS_SELECTOR, 'div.alert.alert-danger.alert-dismissible'
        WebDriverWait(self.driver, timeout=5).until(EC.visibility_of_element_located(locator))

    def wait_text_of_success_review_sending_presence(self) -> None:
        locator = By.CSS_SELECTOR, 'div.alert.alert-success.alert-dismissible'
        WebDriverWait(self.driver, timeout=5).until(EC.visibility_of_element_located(locator))
