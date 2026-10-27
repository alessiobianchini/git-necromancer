import os
from unittest import mock
import pytest
from app.cemetery import DeceasedArtifact
from app.resurrection import generate_resurrection_patch, grant_final_rites


@pytest.fixture
def sample_artifact():
    return DeceasedArtifact(
        id="branch-feat-payment",
        name="feat/payment-gateway",
        artifact_type="BRANCH",
        author="Alessio Bianchini",
        last_commit_hash="8f9a0b1c",
        last_commit_date="2024-02-10T15:00:00+00:00",
        last_commit_message="Add Stripe webhook handlers",
        days_dead=260,
        cause_of_death="Stagnation in staging",
        commits_count=3,
        sample_diff="diff --git a/stripe.py b/stripe.py"
    )


def test_generate_resurrection_patch_protected_branch():
    with pytest.raises(ValueError, match="Cannot resurrect"):
        generate_resurrection_patch(".", "main")


@mock.patch("subprocess.run")
def test_generate_resurrection_patch_success(mock_run):
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "diff --git a/file.py b/file.py\n+new_code = True\n"

    result = generate_resurrection_patch(".", "feat/payment-gateway")
    assert result["success"] is True
    assert "diff --git" in result["patch"]
    assert "git apply" in result["instructions"]


def test_grant_final_rites_memorial_creation(tmp_path, sample_artifact):
    memorial_path = str(tmp_path / "OFRENDA.md")
    epitaph = "Here lies payment-gateway, slain before the sprint ended."

    res = grant_final_rites(
        repo_path=str(tmp_path),
        artifact=sample_artifact,
        epitaph=epitaph,
        memorial_file=memorial_path,
        delete_branch=False
    )

    assert res["success"] is True
    assert os.path.exists(memorial_path)
    with open(memorial_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "feat/payment-gateway" in content
        assert "R.I.P" in content
        assert epitaph in content
        assert "Alessio Bianchini" in content


@mock.patch("subprocess.run")
def test_grant_final_rites_with_branch_deletion(mock_run, tmp_path, sample_artifact):
    mock_run.return_value.returncode = 0
    memorial_path = str(tmp_path / "OFRENDA.md")

    res = grant_final_rites(
        repo_path=str(tmp_path),
        artifact=sample_artifact,
        epitaph="Gone but never forgotten.",
        memorial_file=memorial_path,
        delete_branch=True
    )

    assert res["success"] is True
    assert res["branch_deleted"] is True
    mock_run.assert_called_with(
        ["git", "branch", "-D", "feat/payment-gateway"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        check=False
    )
