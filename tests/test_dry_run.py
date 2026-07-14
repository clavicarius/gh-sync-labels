"""
Test cases for --dry-run feature.
"""

from unittest import mock

from gh_sync_labels import GitHubClient, Label


class TestDryRunMode:
    """Test GitHubClient dry-run mode behavior."""

    def test_dry_run_disabled_by_default(self):
        client = GitHubClient(repository="owner/repo")
        assert client.dry_run is False

    def test_dry_run_enabled(self):
        client = GitHubClient(repository="owner/repo", dry_run=True)
        assert client.dry_run is True

    @mock.patch("subprocess.run")
    def test_dry_run_skips_execution(self, mock_run):
        client = GitHubClient(repository="owner/repo", dry_run=True)
        result = client.run(["label", "create", "bug"])

        mock_run.assert_not_called()
        assert result == ""

    @mock.patch("subprocess.run")
    def test_dry_run_false_executes_subprocess(self, mock_run):
        mock_run.return_value = mock.Mock(returncode=0, stdout="output", stderr="")

        client = GitHubClient(repository="owner/repo", dry_run=False)
        result = client.run(["label", "list"])

        mock_run.assert_called_once()
        assert result == "output"


class TestDryRunIntegration:
    """Integration tests for dry-run with label operations."""

    @mock.patch("subprocess.run")
    def test_create_label_dry_run(self, mock_run):
        from gh_sync_labels import create_label

        client = GitHubClient(repository="owner/repo", dry_run=True)
        label = Label(name="bug", color="D73A4A", description="A bug")

        create_label(client, label)
        mock_run.assert_not_called()

    @mock.patch("subprocess.run")
    def test_update_label_dry_run(self, mock_run):
        from gh_sync_labels import update_label

        client = GitHubClient(repository="owner/repo", dry_run=True)
        label = Label(name="feature", color="1D76DB", description="New feature")

        update_label(client, label)
        mock_run.assert_not_called()

    @mock.patch("subprocess.run")
    def test_delete_label_dry_run(self, mock_run):
        from gh_sync_labels import delete_label

        client = GitHubClient(repository="owner/repo", dry_run=True)
        delete_label(client, "old-label")
        mock_run.assert_not_called()

    @mock.patch("subprocess.run")
    def test_sync_labels_dry_run_counts_created(self, mock_run):
        from gh_sync_labels import sync_labels

        client = GitHubClient(repository="owner/repo", dry_run=True)
        desired = {"bug": Label(name="bug", color="D73A4A", description="Bug")}
        existing = {}

        result = sync_labels(client, desired, existing, overwrite=False)

        assert result.created == 1
        mock_run.assert_not_called()

    @mock.patch("subprocess.run")
    def test_prune_labels_dry_run(self, mock_run):
        from gh_sync_labels import prune_labels

        client = GitHubClient(repository="owner/repo", dry_run=True)
        desired = {"keep": Label(name="keep", color="1D76DB", description="Keep")}
        existing = {
            "keep": Label(name="keep", color="1D76DB", description="Keep"),
            "remove": Label(name="remove", color="CCCCCC", description="Remove"),
        }

        deleted = prune_labels(client, desired, existing)

        assert deleted == 1
        mock_run.assert_not_called()
