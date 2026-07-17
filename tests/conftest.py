"""Shared pytest fixtures: CLI options, driver lifecycle, failure screenshots."""

from __future__ import annotations

import logging
import os

import pytest

from framework.config.config_manager import ConfigManager
from framework.driver.driver_factory import DriverFactory
from framework.utils.screenshot_utils import ScreenshotUtils

logger = logging.getLogger(__name__)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", action="store", default=None, help="Browser to run tests in")
    parser.addoption("--env", action="store", default=None, help="Target environment")
    parser.addoption("--headless", action="store", default=None, help="Run browser headless")


@pytest.fixture(scope="session", autouse=True)
def _apply_cli_overrides(request: pytest.FixtureRequest) -> None:
    """Push --browser/--env/--headless CLI flags into environment variables
    so ConfigManager (which resolves env-var overrides first) picks them up.
    """
    env = request.config.getoption("--env")
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if env:
        os.environ["ENV"] = env
    if browser:
        os.environ["BROWSER"] = browser
    if headless is not None:
        os.environ["HEADLESS"] = headless


@pytest.fixture
def driver(request: pytest.FixtureRequest):
    """Function-scoped WebDriver fixture with automatic teardown and
    on-failure screenshot capture.
    """
    factory = DriverFactory()
    web_driver = factory.create_driver()
    yield web_driver

    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        config = ConfigManager.get_instance()
        ScreenshotUtils.capture(
            web_driver, request.node.name, config.get("screenshot_dir", "screenshots")
        )

    web_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Attach each test phase's report to the item so fixtures can inspect
    pass/fail status during teardown (used by the `driver` fixture above).
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
