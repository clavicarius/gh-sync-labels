"""
Test cases for --export feature.
"""

import csv
from pathlib import Path
from tempfile import TemporaryDirectory

from gh_sync_labels import Label, export_labels, load_labels


class TestExportLabels:
    """Test export_labels function."""

    def test_export_empty_labels(self):
        with TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "labels.csv"
            export_labels({}, output_file)

            with output_file.open("r", encoding="utf-8", newline="") as f:
                rows = list(csv.reader(f, delimiter=";"))

            assert len(rows) == 1
            assert rows[0] == ["Category", "Label", "Color", "Description"]

    def test_export_single_label(self):
        with TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "labels.csv"
            labels = {
                "bug": Label(
                    name="bug",
                    color="D73A4A",
                    description="🐞 A bug that needs fixing",
                )
            }

            export_labels(labels, output_file)

            with output_file.open("r", encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f, delimiter=";"))

            assert len(rows) == 1
            assert rows[0]["Label"] == "bug"
            assert rows[0]["Color"] == "D73A4A"
            assert rows[0]["Description"] == "🐞 A bug that needs fixing"
            assert rows[0]["Category"] == ""

    def test_export_multiple_labels(self):
        with TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "labels.csv"
            labels = {
                "bug": Label(name="bug", color="D73A4A", description="A bug"),
                "feature": Label(name="feature", color="1D76DB", description="A feature"),
                "documentation": Label(name="documentation", color="0075CA", description="Documentation"),
            }

            export_labels(labels, output_file)

            with output_file.open("r", encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f, delimiter=";"))

            assert len(rows) == 3
            names = {row["Label"] for row in rows}
            assert names == {"bug", "feature", "documentation"}

    def test_export_roundtrip_with_load(self):
        with TemporaryDirectory() as tmpdir:
            input_file = Path(tmpdir) / "input.csv"
            input_file.write_text(
                "Category;Label;Color;Description\n"
                ";bug;D73A4A;A bug\n"
                ";feature;1D76DB;A feature\n",
                encoding="utf-8",
            )

            labels = load_labels(input_file)

            output_file = Path(tmpdir) / "output.csv"
            export_labels(labels, output_file)

            reloaded = load_labels(output_file)

            assert set(labels.keys()) == set(reloaded.keys())
            for name in labels:
                assert labels[name].color == reloaded[name].color
                assert labels[name].description == reloaded[name].description
