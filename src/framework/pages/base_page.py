"""Abstract base class for all Page Object Model pages.

Wraps common Selenium interactions with explicit waits so concrete page
objects never need to reach for raw driver calls.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from framework.utils.wait_utils import WaitUtils


class BasePage:
    """Base page object providing wait-wrapped element interactions."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WaitUtils(driver)

    def click(self, locator: tuple[By, str]) -> None:
        self.wait.wait_for_clickable(locator).click()

    def type_text(self, locator: tuple[By, str], text: str, clear_first: bool = True) -> None:
        element = self.wait.wait_for_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[By, str]) -> str:
        return self.wait.wait_for_visible(locator).text

    def is_displayed(self, locator: tuple[By, str]) -> bool:
        try:
            return self.wait.wait_for_visible(locator).is_displayed()
        except Exception:
            return False

    def find(self, locator: tuple[By, str]) -> WebElement:
        return self.wait.wait_for_visible(locator)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_page_title(self) -> str:
        return self.driver.title
