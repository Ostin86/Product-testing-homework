import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from pageobject.add_review_page import AddReviewPage


class AddReviewTest(unittest.TestCase):

    def setUp(self):
        """Действия до теста"""
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
        self.username: str = 'John'
        self.text_with_24_symbols = '24symbol_text...........'
        self.text_with_more_than_24_symbols: str = 'There are more than 25 symbols in this text for review'
        self.text_of_issue_with_rating: str = 'Warning: Please select a review rating!'
        self.text_of_issue_with_review: str = 'Warning: Review Text must be between 25 and 1000 characters!'
        self.text_of_successful_review_adding: str = ('Thank you for your review. It has been submitted to the '
                                                      'webmaster for approval.')

    def tearDown(self):
        self.driver.close()

    def test_review_adding(self):
        """Тест на отправку отзыва без заполнения обязательных для этого полей"""
        add_review_page = AddReviewPage(self.driver)
        add_review_page.open()
        add_review_page.click_on_reviews_tab()
        add_review_page.click_on_continue_button()
        add_review_page.wait_text_of_warning_presence()
        actual_warning_notification: str = add_review_page.get_warning_notification_text()
        expected_result: str = self.text_of_issue_with_rating
        self.assertEqual(actual_warning_notification, expected_result)

    def test_review_options(self):
        """Тест опций ревью"""
        add_review_page = AddReviewPage(self.driver)
        add_review_page.open()
        add_review_page.click_on_reviews_tab()
        add_review_page.click_by_rating_radiobutton()
        add_review_page.clear_your_review_field()
        add_review_page.enter_name_in_name_field(self.username)
        add_review_page.clear_your_review_field()
        add_review_page.enter_text_in_your_review_field(self.text_with_24_symbols)
        add_review_page.click_on_continue_button()
        add_review_page.wait_text_of_warning_presence()
        actual_warning_notification: str = add_review_page.get_warning_notification_text()
        expected_result: str = self.text_of_issue_with_review
        self.assertEqual(actual_warning_notification, expected_result)

    def test_review_approval(self):
        """Тест для подтверждения успешной отправки ревью"""
        add_review_page = AddReviewPage(self.driver)
        add_review_page.open()
        add_review_page.click_on_reviews_tab()
        add_review_page.click_by_rating_radiobutton()
        add_review_page.clear_your_review_field()
        add_review_page.enter_name_in_name_field(self.username)
        add_review_page.clear_your_review_field()
        add_review_page.enter_text_in_your_review_field(self.text_with_more_than_24_symbols)
        add_review_page.click_on_continue_button()
        add_review_page.wait_text_of_success_review_sending_presence()
        actual_result: str = add_review_page.get_message_about_success_review_text()
        expected_result: str = self.text_of_successful_review_adding
        self.assertEqual(actual_result, expected_result)
        pass








