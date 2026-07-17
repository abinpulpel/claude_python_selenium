"""Screenshot capture utility, primarily used from failure hooks."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


class ScreenshotUtils:
    """Captures timestamped PNG screenshots to a configured directory."""

    @staticmethod
    def capture(driver: WebDriver, test_name: str, screenshot_dir: str = "screenshots") -> str:
        """Save a screenshot and return the file path written.

        Args:
            driver: the active WebDriver instance.
            test_name: identifier used in the filename (sanitized).
            screenshot_dir: destination directory, created if missing.
        """
        directory = Path(screenshot_dir)
        directory.mkdir(parents=True, exist_ok=True)

        safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in test_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = directory / f"{safe_name}_{timestamp}.png"

        driver.save_screenshot(str(file_path))
        logger.info("Screenshot captured: %s", file_path)
        return str(file_path)
