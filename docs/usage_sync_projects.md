# Usage Guide (Projects v2)

## Overview

`gh_sync_projects.py` synchronizes GitHub Projects v2 from a CSV configuration directory.

Supported actions:

- create or update a project
- create or update project fields
- synchronize single-select field options
- export existing project configuration
- preview changes without modifying GitHub

---

# Prerequisites

Before using the tool, ensure the following requirements are met.

## Python

Required:

```
Python 3.12+
```

Verify:

```bash
python --version
```

---

## GitHub CLI

The tool uses the GitHub CLI (`gh`) for all repository operations.

Install:

https://cli.github.com/

Verify:

```bash
gh --version
```

---

## Authentication

Authenticate GitHub CLI:

```bash
gh auth login
```

Verify access:

```bash
gh repo view
```

The authenticated user requires permissions to manage repository projects.

---

# Basic Usage (Projects v2)

## Synchronize project definitions

Run:

```bash
python gh_sync_projects.py
```

Default behavior:

- uses the current repository as project scope
- reads `config/projects`
- creates the project if missing
- creates missing fields/options
- leaves existing project settings unchanged unless `--overwrite` is enabled

## Projects configuration layout

Default directory:

```
config/projects/
├── project.csv
├── fields.csv
└── <field-name>.csv
```

- `project.csv`: one row with `Name`, `Description`, `Visibility`
- `fields.csv`: rows with `Name`, `Type`
- `options-*.csv`: optional, only for `single_select` fields; columns `Field`, `Option`, `Color`, `Description`

## Common projects commands

Preview changes:

```bash
python gh_sync_projects.py --dry-run
```

Apply updates to existing metadata/fields/options:

```bash
python gh_sync_projects.py --overwrite
```

Remove fields/options that are no longer defined in CSV:

```bash
python gh_sync_projects.py --overwrite --prune
```

Export an existing project configuration:

```bash
python gh_sync_projects.py --export config/projects-export
```
