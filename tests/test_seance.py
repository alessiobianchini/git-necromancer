from unittest import mock
import pytest
from app.cemetery import DeceasedArtifact
from app.seance import conduct_seance, SeanceResult, build_seance_prompt


@pytest.fixture
def sample_artifact():
    return DeceasedArtifact(
        id="branch-feat-cache",
        name="feat/redis-cache",
        artifact_type="BRANCH",
        author="Devon Vance",
        last_commit_hash="7a8b9c0d",
        last_commit_date="2024-03-01T12:00:00+00:00",
        last_commit_message="Add redis cache pooling",
        days_dead=240,
        cause_of_death="Stagnation in purgatory",
        commits_count=4,
        sample_diff="diff --git a/cache.py b/cache.py\n+import redis"
    )


def test_build_seance_prompt(sample_artifact):
    prompt = build_seance_prompt(sample_artifact)
    assert "feat/redis-cache" in prompt
    assert "Devon Vance" in prompt
    assert "gothic" in prompt.lower() or "ghost" in prompt.lower()


@mock.patch("requests.post")
def test_conduct_seance_with_ollama_success(mock_post, sample_artifact):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": (
            "GHOST MONOLOGUE: I was summoned into existence on March 2024 by Devon. "
            "I dreamed of speeding up database queries, but I was abandoned when the Redis cluster broke.\n"
            "AUTOPSY: High memory usage in staging caused the PR to stall.\n"
            "SUGGESTED ACTION: RESURRECT\n"
            "DIFFICULTY: MEDIUM"
        ),
        "prompt_eval_count": 85,
        "eval_count": 120
    }

    result = conduct_seance(sample_artifact, ollama_url="http://localhost:11434", model="gemma2:2b")
    assert isinstance(result, SeanceResult)
    assert result.artifact_name == "feat/redis-cache"
    assert "Devon" in result.ghost_monologue
    assert result.prompt_tokens == 85
    assert result.completion_tokens == 120
    assert result.suggested_action == "RESURRECT"


@mock.patch("requests.post", side_effect=Exception("Connection refused"))
def test_conduct_seance_fallback_when_ollama_unavailable(mock_post, sample_artifact):
    # Should not raise exception; must generate a witty fallback monologue
    result = conduct_seance(sample_artifact, ollama_url="http://localhost:11434", model="gemma2:2b")
    assert isinstance(result, SeanceResult)
    assert result.artifact_name == "feat/redis-cache"
    assert len(result.ghost_monologue) > 50
    assert "redis" in result.ghost_monologue.lower() or "devon" in result.ghost_monologue.lower()
