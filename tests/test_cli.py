import sys
from unittest import mock
import pytest
from cli import build_parser, main


def test_build_parser_commands():
    parser = build_parser()
    # Test valid subcommands parse without error
    args_scan = parser.parse_args(["scan"])
    assert args_scan.command == "scan"

    args_seance = parser.parse_args(["seance", "feat/foo"])
    assert args_seance.command == "seance"
    assert args_seance.target == "feat/foo"

    args_res = parser.parse_args(["resurrect", "feat/foo", "-o", "custom.patch"])
    assert args_res.command == "resurrect"
    assert args_res.output == "custom.patch"

    args_exo = parser.parse_args(["exorcise", "feat/foo", "--delete"])
    assert args_exo.command == "exorcise"
    assert args_exo.delete is True

    args_web = parser.parse_args(["web", "--port", "9000"])
    assert args_web.command == "web"
    assert args_web.port == 9000


@mock.patch("cli.scan_graveyard")
def test_cli_scan_command(mock_scan, capsys):
    from app.cemetery import DeceasedArtifact
    mock_scan.return_value = [
        DeceasedArtifact(
            id="branch-test",
            name="feat/abandoned",
            artifact_type="BRANCH",
            author="Devon",
            last_commit_hash="1a2b3c",
            last_commit_date="2024-01-01T00:00:00+00:00",
            last_commit_message="WIP",
            days_dead=300,
            cause_of_death="Stagnation",
            commits_count=1,
            sample_diff=""
        )
    ]
    with mock.patch.object(sys, "argv", ["cli.py", "scan"]):
        ret = main()
        assert ret == 0


@mock.patch("cli.conduct_seance")
@mock.patch("cli.scan_graveyard")
def test_cli_seance_command(mock_scan, mock_seance):
    from app.cemetery import DeceasedArtifact
    from app.seance import SeanceResult
    artifact = DeceasedArtifact(
        id="branch-test",
        name="feat/abandoned",
        artifact_type="BRANCH",
        author="Devon",
        last_commit_hash="1a2b3c",
        last_commit_date="2024-01-01T00:00:00+00:00",
        last_commit_message="WIP",
        days_dead=300,
        cause_of_death="Stagnation",
        commits_count=1,
        sample_diff=""
    )
    mock_scan.return_value = [artifact]
    mock_seance.return_value = SeanceResult(
        artifact_id="branch-test",
        artifact_name="feat/abandoned",
        ghost_monologue="I am the ghost of unfinished features.",
        cause_of_death_analysis="Merge conflicts killed me.",
        suggested_action="RESURRECT",
        resurrection_difficulty="MEDIUM",
        prompt_tokens=50,
        completion_tokens=60,
        model_used="gemma2:2b"
    )

    with mock.patch.object(sys, "argv", ["cli.py", "seance", "feat/abandoned"]):
        ret = main()
        assert ret == 0
