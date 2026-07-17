"""Explicit-wait helpers wrapping :class:`WebDriverWait`.

Centralizing waits here keeps page objects free of raw ``time.sleep`` calls
and inconsistent wait conditions.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from framework.config.config_manager import ConfigManager


class WaitUtils:
    """Provides commonly used explicit-wait operations."""

    def __init__(self, driver: WebDriver, timeout: int | None = None) -> None:
        self._driver = driver
        self._timeout = timeout or ConfigManager.get_instance().get_int("explicit_wait", 15)

    def wait_for_visible(self, locator: tuple[By, str]) -> WebElement:
        return WebDriverWait(self._driver, self._timeout).until(
            ec.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator: tuple[By, str]) -> WebElement:
        return WebDriverWait(self._driver, self._timeout).until(
            ec.element_to_be_clickable(locator)
        )

    def wait_for_invisible(self, locator: tuple[By, str]) -> bool:
        return WebDriverWait(self._driver, self._timeout).until(
            ec.invisibility_of_element_located(locator)
        )

    def wait_for_url_contains(self, fragment: str) -> bool:
        return WebDriverWait(self._driver, self._timeout).until(ec.url_contains(fragment))

    def wait_for_title_contains(self, fragment: str) -> bool:
        return WebDriverWait(self._driver, self._timeout).until(ec.title_contains(fragment))
