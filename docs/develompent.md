# Development Guide

## Overview

This document describes how to develop, test, and extend `gh_sync_labels.py`.

The project is intentionally designed as a lightweight DevOps utility:

- minimal dependencies
- clear separation of responsibilities
- easy local execution
- automation-ready
- testable components

---

# Development Requirements

Required:

| Component | Version |
|-|-|
| Python | 3.12+ |
| Git | latest |
| GitHub CLI | latest |
| pytest | latest |

Verify Python:

```bash
python --version
```

Verify GitHub CLI:

```bash
gh --version
```

---

# Local Setup

Clone the repository:

```bash
git clone <repository>
cd <repository>
```

Verify GitHub authentication:

```bash
gh auth status
```

The application itself has no runtime dependencies.

---

# Project Structure

Recommended development structure:

```
.
├── gh_sync_labels.py
├── labels.csv
│
├── tests
│   ├── test_csv_parsing.py
│   └── test_label_comparison.py
│
├── docs
│   ├── usage.md
│   ├── configuration.md
│   ├── architecture.md
│   ├── github-actions.md
│   └── development.md
│
└── .github
    └── workflows
        └── sync-labels.yml
```

---

# Development Workflow

Recommended workflow:

```
Create branch

    |
    v

Implement change

    |
    v

Run tests

    |
    v

Run dry-run

    |
    v

Create Pull Request

    |
    v

Review and merge
```

---

# Running the Application

Basic execution:

```bash
python gh_sync_labels.py
```

Debug mode:

```bash
python gh_sync_labels.py \
  --debug
```

Preview:

```bash
python gh_sync_labels.py \
  --dry-run
```

---

# Testing

The project uses `pytest`.

Install:

```bash
pip install pytest
```

Run all tests:

```bash
pytest -v
```

Expected result:

```
====================

8 passed

====================
```

---

# Test Structure

Tests are separated by responsibility.

```
tests/

├── test_csv_parsing.py

└── test_label_comparison.py
```

---

# CSV Parsing Tests

File:

```
tests/test_csv_parsing.py
```

Covers:

- valid CSV loading
- missing columns
- invalid colors
- duplicate labels
- UTF-8 handling
- emoji support

Example:

```python
def test_color_normalization():

    assert normalize_color(
        "#d73a4a"
    ) == "D73A4A"
```

---

# Comparison Logic Tests

File:

```
tests/test_label_comparison.py
```

Covers:

- identical labels
- changed colors
- changed descriptions

Example:

```python
assert labels_equal(
    current,
    desired,
)
```

---

# Test Principles

Tests should:

- avoid real GitHub repositories
- avoid network access
- use temporary files
- validate business logic independently

The GitHub CLI layer should be mocked for integration tests.

---

# Coding Guidelines

## Python Style

Follow:

- PEP 8
- type hints
- descriptive names
- small functions

Example:

Good:

```python
def load_labels(
    csv_file: Path
) -> dict[str, Label]:
```

Avoid:

```python
def load(x):
```

---

# Type Hints

All public functions should define:

- parameter types
- return types

Example:

```python
def delete_label(
    client: GitHubClient,
    label_name: str,
) -> None:
```

---

# Logging

Use the project logger:

```python
logger.info(
    "Creating label: %s",
    label.name,
)
```

Avoid:

```python
print()
```

Logging levels:

| Level | Usage |
|-|-|
| DEBUG | Internal details |
| INFO | Normal operation |
| WARNING | Recoverable issues |
| ERROR | Failures |

---

# Error Handling

Errors should:

- provide meaningful messages
- fail with exit code `1`
- not expose secrets

Example:

Good:

```
Invalid CSV row 12:
Missing description
```

Avoid:

```
Error
```

---

# Adding New Features

When extending the application:

Follow the component structure.

Example:

Adding YAML support:

Current:

```
CSV Loader
```

Add:

```
YAML Loader
```

Keep:

```
Label Model
Synchronization Engine
GitHub Client
```

unchanged.

---

# Adding New CLI Options

New options should:

1. be added in `parse_arguments()`
2. have documentation in `docs/usage.md`
3. include tests where applicable

Example:

```python
parser.add_argument(
    "--new-option"
)
```

---

# Integration Testing

For integration tests:

Use a temporary repository.

Recommended approach:

```
Test Repository

      |
      v

Run gh_sync_labels.py

      |
      v

Verify labels

      |
      v

Cleanup
```

Do not run integration tests against production repositories.

---

# Debugging

Enable debug logging:

```bash
python gh_sync_labels.py \
  --debug
```

Typical debugging steps:

1. validate CSV
2. run dry-run
3. check GitHub authentication
4. verify permissions

---

# Release Process

Recommended release flow:

```
Feature complete

      |
      v

Run tests

      |
      v

Update CHANGELOG.md

      |
      v

Create tag

      |
      v

Release
```

Example:

```bash
git tag v1.0.0
git push --tags
```

---

# Contribution Guidelines

Before submitting changes:

Ensure:

- tests pass
- documentation is updated
- code follows existing style
- new features include tests

Pull Requests should describe:

- what changed
- why it changed
- how it was tested

---

# Continuous Integration

Recommended CI pipeline:

```
Pull Request

    |
    +--> pytest

    |
    +--> CSV validation

    |
    +--> dry-run validation
```

Example checks:

```bash
pytest -v

python gh_sync_labels.py \
  --dry-run
```

---

# Future Development Areas

Potential improvements:

## Configuration

- YAML support
- JSON support
- schema validation

## Synchronization

- organization-wide sync
- protected labels
- label ownership
- automatic drift reports

## Testing

- GitHub API mocks
- integration environment
- coverage reporting

## Automation

- reusable GitHub Action
- Marketplace publication
- scheduled compliance checks

---

# Development Philosophy

The project follows these principles:

| Principle | Meaning |
|-|-|
| Simple | Avoid unnecessary complexity |
| Automated | Reduce manual maintenance |
| Testable | Keep logic independent |
| Transparent | Show planned changes |
| Safe | Never delete without explicit intent |
