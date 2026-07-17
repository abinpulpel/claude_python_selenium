# Contributing to claude_python_selenium

Thank you for considering a contribution to this framework. This document
outlines the process and standards for contributing.

## Prerequisites

- Python 3.13+
- Google Chrome and/or Mozilla Firefox installed locally
- Git

## Getting Started

1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the sample suite: `pytest -m smoke`

## Running Tests

```bash
# Full suite
pytest

# Smoke suite only
pytest -m smoke

# Specific browser / environment
pytest --browser=firefox --env=staging

# Parallel execution across 4 workers
pytest -n 4

# Headless execution
pytest --headless=true
```

## Gherkin / Style Guide

This is a plain pytest framework (no Gherkin). Test names must be descriptive
and prefixed with `test_`. Page objects live under `src/framework/pages/` and
must only expose business-readable methods (no raw Selenium calls in test
files).

## Branching & Commits

- Branch naming: `feature/<short-description>`, `fix/<short-description>`
- Commit messages: imperative mood, e.g. `Add retry logic to WaitUtils`
- One logical change per commit

## Code Standards

- Format with `black`, lint with `ruff`
- Type-hint all public methods
- Docstrings (Google style) on all public classes and methods
- No hard-coded waits (`time.sleep`) — use `WaitUtils`

## Pull Request Checklist

- [ ] Tests pass locally (`pytest`)
- [ ] New/changed behavior has test coverage
- [ ] README/CHANGELOG updated if behavior changes
- [ ] No linter warnings (`ruff check .`)

## Reporting Issues

Please open a GitHub issue with steps to reproduce, expected vs. actual
behavior, and environment details (OS, Python version, browser).
