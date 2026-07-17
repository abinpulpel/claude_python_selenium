# claude_python_selenium

Reusable, enterprise-grade **Python + Selenium** automation framework built on
the **Page Object Model**. Designed so QA engineers can immediately start
writing automated tests by importing existing configuration, driver
management, page objects, and utility classes — no boilerplate required.

## Overview

This framework provides a production-ready foundation for UI test automation:

- Layered YAML configuration (base + per-environment overrides), with
  environment-variable and CLI-flag overrides on top.
- A `DriverFactory` supporting Chrome, Firefox, Edge, and Safari, locally or
  against a remote Selenium Grid.
- A `BasePage` with explicit-wait wrapped interactions — no raw Selenium calls
  or hard-coded sleeps in page objects or tests.
- Pytest fixtures for driver lifecycle, CLI options (`--browser`, `--env`,
  `--headless`), and automatic on-failure screenshots.
- A `DataReader` utility supporting JSON, YAML, CSV, and Excel test data.
- Parallel execution via `pytest-xdist`, HTML reporting via `pytest-html`.
- Docker and Selenium Grid (`docker-compose.yml`) support for containerized
  and cross-browser execution.
- GitHub Actions CI with a Chrome/Firefox execution matrix.

## Architecture

```
Test Layer (tests/)
   -> Page Objects (src/framework/pages/)
        -> Base Page (wait-wrapped interactions)
             -> WaitUtils / Selenium WebDriver
   -> DriverFactory (creates WebDriver per ConfigManager)
   -> ConfigManager (layered YAML + env var resolution)
```

Design principles: Page Object Model, Factory Pattern (driver creation),
Singleton (config manager), Dependency Injection (fixtures), composition over
inheritance, and single-responsibility utility classes.

## Folder Structure

```
claude_python_selenium/
├── config/                        # Base + per-environment YAML configuration
├── src/framework/
│   ├── config/config_manager.py   # Layered configuration singleton
│   ├── driver/driver_factory.py   # WebDriver creation (local + remote)
│   ├── enums/browser_type.py      # Supported browser enum
│   ├── exceptions/                # Framework exception hierarchy
│   ├── pages/                     # BasePage + sample LoginPage/HomePage
│   └── utils/                     # Wait, screenshot, and data-reader utilities
├── tests/
│   ├── conftest.py                # Fixtures: driver, CLI options, screenshots
│   ├── data/login_data.json       # Sample data-driven test data
│   └── test_login.py              # Sample smoke/regression/data-driven tests
├── .github/workflows/ci.yml       # CI: Chrome/Firefox matrix
├── Dockerfile / docker-compose.yml
├── pytest.ini / pyproject.toml
└── requirements.txt
```

## Technology Stack

| Concern           | Choice                              |
|--------------------|--------------------------------------|
| Language           | Python 3.13+                        |
| Browser automation | Selenium 4.27+                      |
| Test runner        | pytest 8.x                          |
| Parallel execution | pytest-xdist                        |
| Reporting          | pytest-html                         |
| Config format      | YAML (PyYAML)                       |
| Data-driven        | JSON, YAML, CSV, Excel (openpyxl)   |
| Containerization   | Docker, Selenium Grid               |
| CI/CD              | GitHub Actions                      |

## Installation

### Prerequisites

- Python 3.13 or later
- Google Chrome and/or Mozilla Firefox
- Docker (optional, for Grid/containerized execution)

### Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Configuration is layered: `config/config.yaml` provides defaults, and
`config/config-<env>.yaml` overrides them per environment (`qa`, `staging`,
`prod`). Any key can also be overridden via an environment variable of the
same name (uppercased), or via the `--browser` / `--env` / `--headless`
pytest CLI flags.

## Execution

```bash
# Full suite, default environment (qa)
pytest

# Smoke suite only
pytest -m smoke

# Specific browser and environment
pytest --browser=firefox --env=staging

# Headless execution
pytest --headless=true
```

### Parallel Execution

```bash
pytest -n 4
```

### Cross-Browser

Run the same suite against multiple browsers by invoking pytest once per
`--browser` value (see `.github/workflows/ci.yml` for a matrix example).

### Docker / Selenium Grid

```bash
docker compose up --build
```

Spins up a Selenium Hub, Chrome and Firefox nodes, and a test-runner container
configured for remote execution against the Grid.

### CI/CD

`.github/workflows/ci.yml` runs the suite across a Chrome/Firefox matrix on
every push and pull request, uploading the HTML report, screenshots, and logs
as build artifacts.

## Reporting

HTML reports are written to `reports/report.html` via `pytest-html`
(`--self-contained-html`, configured in `pytest.ini`).

## Logging

Standard library `logging` is used throughout; configure verbosity via
`log_cli_level` in `pytest.ini` or your own `logging.conf`.

## Troubleshooting

- **`ModuleNotFoundError: framework`**: ensure `pytest.ini`'s `pythonpath = src`
  is picked up (run pytest from the repository root).
- **Driver/browser version mismatch**: `webdriver-manager` resolves matching
  driver binaries automatically; ensure the browser itself is installed.
- **Remote Grid connection refused**: confirm `remote_grid_url` matches the
  hub's exposed port (`4444` by default).

## Contribution Guide

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, branching, and PR standards.

## License

Distributed under the [MIT License](LICENSE).

## Roadmap

- Allure reporting adapter
- BrowserStack / LambdaTest cloud execution profiles
- Visual regression testing hooks
- Accessibility (axe-core) integration
