"""Sample page object for the application login screen."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from framework.pages.base_page import BasePage
from framework.pages.home_page import HomePage


class LoginPage(BasePage):
    """Represents the login page and its available user actions."""

    _USERNAME_INPUT = (By.ID, "username")
    _PASSWORD_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def enter_username(self, username: str) -> "LoginPage":
        self.type_text(self._USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.type_text(self._PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        self.click(self._LOGIN_BUTTON)

    def login(self, username: str, password: str) -> HomePage:
        """Fluent login helper returning the resulting :class:`HomePage`."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return HomePage(self.driver)

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_displayed(self._ERROR_MESSAGE)
