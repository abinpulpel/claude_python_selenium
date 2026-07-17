# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-17

### Added

- Initial Python Selenium Page Object Model framework scaffold.
- `ConfigManager` for layered YAML configuration (base + environment overrides).
- `DriverFactory` supporting Chrome, Firefox, and Edge, local and remote (Selenium Grid) execution.
- `BasePage` with explicit-wait wrapped interaction methods.
- Sample `LoginPage` and `HomePage` page objects.
- `WaitUtils` explicit-wait helper utilities.
- `ScreenshotUtils` for automatic on-failure screenshot capture.
- `DataReader` utility supporting JSON, YAML, CSV, and Excel data sources.
- Pytest fixtures (`conftest.py`) for driver lifecycle, CLI options, and failure-screenshot hooks.
- Sample data-driven login test suite (`test_login.py`) with smoke and regression markers.
- Parallel execution support via `pytest-xdist`.
- HTML reporting via `pytest-html`.
- Dockerfile and docker-compose Selenium Grid setup.
- GitHub Actions CI workflow with a Chrome/Firefox browser matrix.
- Project governance docs: README, CONTRIBUTING, CODE_OF_CONDUCT, LICENSE.
