from datetime import datetime, timezone, timedelta
from unittest import mock
import pytest
from app.cemetery import DeceasedArtifact, scan_graveyard, get_mock_graveyard


def test_deceased_artifact_model():
    artifact = DeceasedArtifact(
        id="branch-feat-old",
        name="feat/old-auth",
        artifact_type="BRANCH",
        author="Alessio Bianchini",
        last_commit_hash="a1b2c3d4e5",
        last_commit_date="2024-03-01T12:00:00+00:00",
        last_commit_message="WIP auth flow",
        days_dead=240,
        cause_of_death="Stagnation (>90 days in purgatory)",
        commits_count=5,
        sample_diff="diff --git a/auth.py b/auth.py..."
    )
    assert artifact.name == "feat/old-auth"
    assert artifact.days_dead == 240
    assert artifact.artifact_type == "BRANCH"


def test_get_mock_graveyard():
    mock_items = get_mock_graveyard()
    assert len(mock_items) >= 3
    branch_names = [item.name for item in mock_items]
    assert any("legacy" in name or "experiment" in name or "auth" in name for name in branch_names)
    assert all(item.days_dead > 30 for item in mock_items)


def test_scan_graveyard_empty_or_non_git():
    # If invalid path, should return empty list or fallback to mock if demo mode
    result = scan_graveyard("/invalid/non_existent_directory_xyz")
    assert isinstance(result, list)


@mock.patch("subprocess.run")
def test_scan_graveyard_git_branches(mock_run):
    # Mock git branch output
    def side_effect(cmd, *args, **kwargs):
        class MockProcess:
            returncode = 0
            def __init__(self, stdout):
                self.stdout = stdout

        if "branch" in cmd:
            return MockProcess("  feat/ancient-cache\n* master\n  experiment/legacy-worker\n")
        elif "log" in cmd:
            return MockProcess("9f8e7d6c|2024-01-15T10:00:00+00:00|Alessio Bianchini|Add redis caching prototype\n")
        elif "stash" in cmd:
            return MockProcess("stash@{0}|2024-02-10T14:30:00+00:00|WIP on quick hotfix\n")
        elif "diff" in cmd or "show" in cmd:
            return MockProcess("diff --git a/cache.py b/cache.py\n+import redis\n")
        return MockProcess("")

    mock_run.side_effect = side_effect
    ref_date = datetime(2024, 10, 27, tzinfo=timezone.utc)
    artifacts = scan_graveyard(".", reference_date=ref_date)
    assert len(artifacts) >= 1
    branch_names = [a.name for a in artifacts]
    assert "feat/ancient-cache" in branch_names
    assert artifacts[0].days_dead > 200
