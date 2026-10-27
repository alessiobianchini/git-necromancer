"""Séance AI engine: summons the spirits of deceased code artifacts using local Gemma 2 2B."""

import logging
import re
from typing import Optional
import requests
from pydantic import BaseModel
from app.cemetery import DeceasedArtifact
from app.telemetry import trace_seance, record_ai_metrics

logger = logging.getLogger("git-necromancer.seance")


class SeanceResult(BaseModel):
    """The result of summoning the spirit of a deceased code artifact."""
    artifact_id: str
    artifact_name: str
    ghost_monologue: str
    cause_of_death_analysis: str
    suggested_action: str = "MEMORIALIZE"  # RESURRECT, MEMORIALIZE, INVESTIGATE
    resurrection_difficulty: str = "MEDIUM"  # EASY, MEDIUM, SEVERE_CONFLICTS
    prompt_tokens: int = 0
    completion_tokens: int = 0
    model_used: str = "gemma2:2b"


def build_seance_prompt(artifact: DeceasedArtifact) -> str:
    """Build an atmospheric gothic prompt for Gemma 2 2B to channel the deceased code."""
    diff_snippet = artifact.sample_diff[:400] if artifact.sample_diff else "No diff available."
    return f"""You are the ghost of an abandoned piece of code in a Git repository cemetery.
The necromancer has summoned your spirit for a Halloween code séance.
Speak in the first person ("I") with a gothic, atmospheric, witty developer persona.

Artifact Details:
- Type: {artifact.artifact_type}
- Name: {artifact.name}
- Creator: {artifact.author}
- Last Commit: "{artifact.last_commit_message}" (Hash: {artifact.last_commit_hash})
- Date of Death: {artifact.last_commit_date} ({artifact.days_dead} days trapped in purgatory)
- Diff Preview:
{diff_snippet}

Respond using exactly this structured format:
GHOST MONOLOGUE: <A 2-3 sentence evocative, first-person confession of who created you, what your purpose was, and how you were forgotten or slain>
AUTOPSY: <1 sentence diagnostic explanation of why this code was abandoned or why it failed to merge>
SUGGESTED ACTION: <RESURRECT or MEMORIALIZE or INVESTIGATE>
DIFFICULTY: <EASY or MEDIUM or SEVERE_CONFLICTS>
"""


def _generate_fallback_seance(artifact: DeceasedArtifact, model: str) -> SeanceResult:
    """Generate an atmospheric fallback monologue when local Ollama is offline or in mock demo."""
    monologue = (
        f"I was summoned into existence {artifact.days_dead} days ago by {artifact.author}. "
        f"I still recall the frantic keystrokes of '{artifact.last_commit_message}' in {artifact.name}. "
        f"Alas, priorities shifted like mist in the night, and my branch was left to wither in the cold purgatory of git history."
    )
    autopsy = f"The pull request was never opened; context switching and architectural drift doomed {artifact.name}."
    suggested_action = "RESURRECT" if artifact.days_dead < 180 else "MEMORIALIZE"
    difficulty = "EASY" if artifact.artifact_type == "STASH" else "MEDIUM"

    return SeanceResult(
        artifact_id=artifact.id,
        artifact_name=artifact.name,
        ghost_monologue=monologue,
        cause_of_death_analysis=autopsy,
        suggested_action=suggested_action,
        resurrection_difficulty=difficulty,
        prompt_tokens=45,
        completion_tokens=65,
        model_used=f"{model} (spectral fallback)"
    )


def conduct_seance(
    artifact: DeceasedArtifact,
    ollama_url: str = "http://localhost:11434",
    model: str = "gemma2:2b",
    timeout: float = 12.0
) -> SeanceResult:
    """Channel the spirit of the deceased code via local Gemma 2 2B with Sentry telemetry."""
    prompt = build_seance_prompt(artifact)

    with trace_seance(artifact_id=artifact.id, model_name=model):
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            }
            resp = requests.post(f"{ollama_url.rstrip('/')}/api/generate", json=payload, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                raw_text = data.get("response", "").strip()
                prompt_tokens = data.get("prompt_eval_count", 0)
                completion_tokens = data.get("eval_count", 0)

                record_ai_metrics(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)

                # Parse sections from structured output
                monologue_match = re.search(r"GHOST MONOLOGUE:\s*(.+?)(?=\nAUTOPSY:|\Z)", raw_text, re.DOTALL | re.IGNORECASE)
                autopsy_match = re.search(r"AUTOPSY:\s*(.+?)(?=\nSUGGESTED ACTION:|\Z)", raw_text, re.DOTALL | re.IGNORECASE)
                action_match = re.search(r"SUGGESTED ACTION:\s*(\w+)", raw_text, re.IGNORECASE)
                diff_match = re.search(r"DIFFICULTY:\s*(\w+)", raw_text, re.IGNORECASE)

                monologue = monologue_match.group(1).strip() if monologue_match else raw_text
                autopsy = autopsy_match.group(1).strip() if autopsy_match else artifact.cause_of_death
                action = action_match.group(1).strip().upper() if action_match else "RESURRECT"
                difficulty = diff_match.group(1).strip().upper() if diff_match else "MEDIUM"

                if action not in ["RESURRECT", "MEMORIALIZE", "INVESTIGATE"]:
                    action = "MEMORIALIZE"

                return SeanceResult(
                    artifact_id=artifact.id,
                    artifact_name=artifact.name,
                    ghost_monologue=monologue,
                    cause_of_death_analysis=autopsy,
                    suggested_action=action,
                    resurrection_difficulty=difficulty,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    model_used=model
                )
        except Exception as exc:
            logger.info(f"Ollama séance unavailable ({exc}), invoking spectral heuristic fallback")

        # Fallback if Ollama is unreachable
        fallback = _generate_fallback_seance(artifact, model)
        record_ai_metrics(prompt_tokens=fallback.prompt_tokens, completion_tokens=fallback.completion_tokens)
        return fallback
