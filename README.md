# GitHub Label Synchronization Tool (gh-sync-labels)

Synchronize GitHub repository labels from a CSV configuration.

![logo](./assets/logo.png)

`gh_sync_labels` treats the CSV file as the single source of truth and keeps GitHub repository labels synchronized.

## Features

- Create missing labels
- Update existing labels
- Remove obsolete labels
- Export existing labels
- Dry-run support
- CSV validation
- GitHub Actions support
- UTF-8 and emoji support

## Requirements

- Python 3.12+
- GitHub CLI (`gh`)
- Authenticated GitHub session

## Quick Start

Clone repository:

```bash
git clone <repository>
cd <repository>
````

Run:

```bash
python gh_sync_labels.py
```

Full synchronization:

```bash
python gh_sync_labels.py \
  --overwrite \
  --prune
```

## Documentation

Detailed documentation:

* [Usage](docs/usage.md)
* [Configuration](docs/configuration.md)
* [Architecture](docs/architecture.md)
* [GitHub Actions](docs/github-actions.md)
* [Development](docs/development.md)

## License

MIT
