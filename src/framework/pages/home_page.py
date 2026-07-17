"""Sample page object for the authenticated landing page."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from framework.pages.base_page import BasePage


class HomePage(BasePage):
    """Represents the post-login landing page."""

    _WELCOME_BANNER = (By.CSS_SELECTOR, ".welcome-banner")
    _LOGOUT_LINK = (By.ID, "logout")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def is_welcome_banner_displayed(self) -> bool:
        return self.is_displayed(self._WELCOME_BANNER)

    def get_welcome_text(self) -> str:
        return self.get_text(self._WELCOME_BANNER)

    def logout(self) -> "LoginPage":
        from framework.pages.login_page import LoginPage

        self.click(self._LOGOUT_LINK)
        return LoginPage(self.driver)
