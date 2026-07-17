"""Root exception hierarchy for the framework."""

from __future__ import annotations


class FrameworkException(Exception):
    """Base unchecked exception raised by framework internals.

    Test code should let this propagate rather than catching it, unless a
    specific recovery path exists.
    """

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.__cause__ = cause
