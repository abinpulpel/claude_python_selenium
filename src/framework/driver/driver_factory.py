"""Factory responsible for creating configured :class:`WebDriver` instances.

Supports local execution (Chrome/Firefox/Edge/Safari) and remote execution
against a Selenium Grid endpoint, driven entirely by :class:`ConfigManager`.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from framework.config.config_manager import ConfigManager
from framework.enums.browser_type import BrowserType
from framework.exceptions.framework_exceptions import FrameworkException


class DriverFactory:
    """Creates :class:`WebDriver` instances based on the active configuration."""

    def __init__(self, config: ConfigManager | None = None) -> None:
        self._config = config or ConfigManager.get_instance()

    def create_driver(self, browser: str | None = None) -> WebDriver:
        """Create a new WebDriver instance for the given (or configured) browser."""
        browser_type = BrowserType.from_string(browser or self._config.get("browser", "chrome"))
        headless = self._config.get_bool("headless", False)
        remote = self._config.get_bool("remote_execution", False)

        if remote:
            return self._create_remote_driver(browser_type, headless)
        return self._create_local_driver(browser_type, headless)

    def _create_local_driver(self, browser_type: BrowserType, headless: bool) -> WebDriver:
        match browser_type:
            case BrowserType.CHROME:
                return webdriver.Chrome(options=self._chrome_options(headless))
            case BrowserType.FIREFOX:
                return webdriver.Firefox(options=self._firefox_options(headless))
            case BrowserType.EDGE:
                return webdriver.Edge(options=self._edge_options(headless))
            case BrowserType.SAFARI:
                return webdriver.Safari()
            case _:
                raise FrameworkException(f"No local driver strategy for {browser_type}")

    def _create_remote_driver(self, browser_type: BrowserType, headless: bool) -> WebDriver:
        grid_url = self._config.get("remote_grid_url")
        if not grid_url:
            raise FrameworkException("remote_grid_url must be set for remote execution")

        options_by_browser = {
            BrowserType.CHROME: self._chrome_options(headless),
            BrowserType.FIREFOX: self._firefox_options(headless),
            BrowserType.EDGE: self._edge_options(headless),
        }
        options = options_by_browser.get(browser_type)
        if options is None:
            raise FrameworkException(f"No remote driver strategy for {browser_type}")

        return webdriver.Remote(command_executor=grid_url, options=options)

    @staticmethod
    def _chrome_options(headless: bool) -> ChromeOptions:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        return options

    @staticmethod
    def _firefox_options(headless: bool) -> FirefoxOptions:
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return options

    @staticmethod
    def _edge_options(headless: bool) -> EdgeOptions:
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        return options
