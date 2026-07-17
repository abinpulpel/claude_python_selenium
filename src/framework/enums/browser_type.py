"""Supported browser types for the DriverFactory."""

from __future__ import annotations

from enum import Enum

from framework.exceptions.framework_exceptions import FrameworkException


class BrowserType(Enum):
    """Enumerates browsers supported by :class:`DriverFactory`."""

    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"

    @classmethod
    def from_string(cls, value: str) -> "BrowserType":
        """Case-insensitively resolve a string to a :class:`BrowserType`.

        Raises:
            FrameworkException: if ``value`` does not match a supported browser.
        """
        normalized = (value or "").strip().lower()
        for member in cls:
            if member.value == normalized:
                return member
        supported = ", ".join(member.value for member in cls)
        raise FrameworkException(
            f"Unsupported browser '{value}'. Supported values: {supported}"
        )
