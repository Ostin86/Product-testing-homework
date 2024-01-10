import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pageobject.product_page import ProductPage
from webdriver_factory import WebDriverFactory


class AddReviewTest(unittest.TestCase):
    username: str = 'John'
    text_with_24_symbols = '24symbol_text...........'
    text_with_more_than_24_symbols: str = 'There are more than 25 symbols in this text for review'
    text_of_issue_with_rating: str = 'Warning: Please select a review rating!'
    text_of_issue_with_review: str = 'Warning: Review Text must be between 25 and 1000 characters!'
    text_of_successful_review_adding: str = ('Thank you for your review. It has been submitted to the '
                                                  'webmaster for approval.')

    def setUp(self):
        """Действия до теста"""
        self.driver = self.driver = WebDriverFactory.get_driver()
        self.product_id: str = '42'
        self.product_page = ProductPage(self.driver, self.product_id)
        self.product_page.open()
        self.product_page.click_on_reviews_tab()

    def tearDown(self):
        self.driver.close()

    def test_review_adding(self):
        """Тест на отправку отзыва без заполнения обязательных для этого полей"""
        self.product_page.click_on_continue_button()
        actual_warning_notification: str = self.product_page.get_warning_notification_text()
        expected_result: str = self.text_of_issue_with_rating
        self.assertEqual(actual_warning_notification, expected_result)

    def test_review_options(self):
        """Тест опций ревью"""
        self.product_page.click_by_rating_radiobutton()
        self.product_page.clear_your_review_field()
        self.product_page.enter_name_in_name_field(self.username)
        self.product_page.clear_your_review_field()
        self.product_page.enter_text_in_your_review_field(self.text_with_24_symbols)
        self.product_page.click_on_continue_button()
        actual_warning_notification: str = self.product_page.get_warning_notification_text()
        expected_result: str = self.text_of_issue_with_review
        self.assertEqual(actual_warning_notification, expected_result)

    def test_review_approval(self):
        """Тест для подтверждения успешной отправки ревью"""
        self.product_page.click_by_rating_radiobutton()
        self.product_page.clear_your_review_field()
        self.product_page.enter_name_in_name_field(self.username)
        self.product_page.clear_your_review_field()
        self.product_page.enter_text_in_your_review_field(self.text_with_more_than_24_symbols)
        self.product_page.click_on_continue_button()
        actual_result: str = self.product_page.get_message_about_success_review_text()
        expected_result: str = self.text_of_successful_review_adding
        self.assertEqual(actual_result, expected_result)










