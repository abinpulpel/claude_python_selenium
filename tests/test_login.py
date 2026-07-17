"""Sample login test suite demonstrating smoke, regression, and
data-driven scenarios built on top of the reusable framework.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from framework.config.config_manager import ConfigManager
from framework.pages.login_page import LoginPage
from framework.utils.data_reader import DataReader

_DATA_FILE = Path(__file__).parent / "data" / "login_data.json"


@pytest.mark.smoke
def test_successful_login_with_valid_credentials(driver):
    base_url = ConfigManager.get_instance().get("base_url")
    driver.get(base_url)

    home_page = LoginPage(driver).login("standard_user", "correct_password")

    assert home_page.is_welcome_banner_displayed()


@pytest.mark.regression
def test_unsuccessful_login_with_invalid_credentials(driver):
    base_url = ConfigManager.get_instance().get("base_url")
    driver.get(base_url)

    login_page = LoginPage(driver)
    login_page.enter_username("standard_user")
    login_page.enter_password("wrong_password")
    login_page.click_login()

    assert login_page.is_error_displayed()


@pytest.mark.regression
@pytest.mark.parametrize("record", DataReader.read_json(str(_DATA_FILE)))
def test_data_driven_login_attempts(driver, record):
    base_url = ConfigManager.get_instance().get("base_url")
    driver.get(base_url)

    login_page = LoginPage(driver)
    login_page.enter_username(record["username"])
    login_page.enter_password(record["password"])
    login_page.click_login()

    if record["result"] == "success":
        from framework.pages.home_page import HomePage

        assert HomePage(driver).is_welcome_banner_displayed()
    else:
        assert login_page.is_error_displayed()
