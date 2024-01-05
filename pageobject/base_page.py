from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    """Базовый (родительский) класс PageObject, который содержит общие для всех страниц методы"""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def get_url(self) -> str:
        """Обязательно реализовать в дочерних классах. Метод, необходимый для задания url каждой страницы"""
        raise NotImplementedError

    def open(self):
        """Метод для открытия страницы"""
        self.driver.get(self.get_url())

    def save_screenshot(self):
        pass
