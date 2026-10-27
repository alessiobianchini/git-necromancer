"""Git cemetery scanner: discovers abandoned branches, stashes, and dead code artifacts."""

import os
import re
import subprocess
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class DeceasedArtifact(BaseModel):
    """Represents a dead or abandoned code artifact in the repo cemetery."""
    id: str
    name: str
    artifact_type: str = "BRANCH"  # BRANCH, STASH, ZOMBIE
    author: str
    last_commit_hash: str
    last_commit_date: str
    last_commit_message: str
    days_dead: int
    cause_of_death: str
    commits_count: int = 1
    sample_diff: str = ""


def get_mock_graveyard() -> List[DeceasedArtifact]:
    """Return a curated cemetery of realistic dead branches and stashes for demos and testing."""
    return [
        DeceasedArtifact(
            id="branch-feat-graphql-migration",
            name="feat/graphql-migration",
            artifact_type="BRANCH",
            author="Devon Vance",
            last_commit_hash="7f3c2a1e",
            last_commit_date="2024-02-14T18:22:00+00:00",
            last_commit_message="WIP: switch users endpoint to GraphQL schema",
            days_dead=255,
            cause_of_death="Architecture churn: team decided REST + OpenAPI was enough",
            commits_count=8,
            sample_diff="diff --git a/schema.graphql b/schema.graphql\n+type User { id: ID!, name: String! }"
        ),
        DeceasedArtifact(
            id="branch-experiment-redis-layer",
            name="experiment/redis-layer",
            artifact_type="BRANCH",
            author="Sarah Connor",
            last_commit_hash="4a9d8b7c",
            last_commit_date="2024-04-03T11:45:00+00:00",
            last_commit_message="Add multi-tenant redis cache clustering",
            days_dead=207,
            cause_of_death="Memory leak in staging: rolled back and forgotten",
            commits_count=12,
            sample_diff="diff --git a/cache/redis.py b/cache/redis.py\n+import redis.asyncio as aioredis"
        ),
        DeceasedArtifact(
            id="stash-0-auth-token-patch",
            name="stash@{0}",
            artifact_type="STASH",
            author="Alessio Bianchini",
            last_commit_hash="9e1f2c3d",
            last_commit_date="2024-05-19T23:10:00+00:00",
            last_commit_message="WIP on jwt refresh rotation bugfix",
            days_dead=161,
            cause_of_death="Interrupted hotfix: developer switched branches and forgot",
            commits_count=1,
            sample_diff="diff --git a/auth/jwt.py b/auth/jwt.py\n+def rotate_refresh_token(token): pass"
        ),
        DeceasedArtifact(
            id="branch-feat-v2-dashboard-ui",
            name="feat/v2-dashboard-ui",
            artifact_type="BRANCH",
            author="Marcus Brody",
            last_commit_hash="3c4d5e6f",
            last_commit_date="2024-01-10T14:15:00+00:00",
            last_commit_message="Redesign dashboard metrics with D3 chart components",
            days_dead=290,
            cause_of_death="Product pivot: design requirements changed completely",
            commits_count=15,
            sample_diff="diff --git a/frontend/d3_charts.js b/frontend/d3_charts.js\n+export function renderGothicDonut() {}"
        ),
    ]


def _parse_iso_date(date_str: str) -> datetime:
    """Safely parse ISO date strings from git log."""
    try:
        # Handles 2024-01-15T10:00:00+00:00 or with Z
        cleaned = date_str.strip().replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned)
    except Exception:
        return datetime.now(timezone.utc)


def scan_graveyard(
    repo_path: str = ".",
    reference_date: Optional[datetime] = None,
    stale_days_threshold: int = 30
) -> List[DeceasedArtifact]:
    """Scan a git repository for dead branches, stashes, and stale artifacts."""
    if not os.path.isdir(repo_path):
        return []

    if reference_date is None:
        reference_date = datetime.now(timezone.utc)

    artifacts: List[DeceasedArtifact] = []

    # 1. Inspect Branches
    try:
        # List branches
        branch_proc = subprocess.run(
            ["git", "branch", "--list"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )

        if branch_proc.returncode == 0 and branch_proc.stdout:
            lines = branch_proc.stdout.strip().split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Ignore current HEAD branch indicator '*'
                is_active = line.startswith("*")
                branch_name = line.lstrip("* ").strip()

                # Skip main and master from dead branches
                if branch_name in ["main", "master"] or is_active:
                    continue

                # Get latest commit info for this branch
                log_proc = subprocess.run(
                    ["git", "log", "-1", "--format=%H|%aI|%an|%s", branch_name],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    check=False
                )

                if log_proc.returncode == 0 and log_proc.stdout.strip():
                    parts = log_proc.stdout.strip().split("|", 3)
                    if len(parts) == 4:
                        commit_hash, date_str, author, message = parts
                        commit_dt = _parse_iso_date(date_str)
                        days_dead = max(0, (reference_date - commit_dt).days)

                        if days_dead >= stale_days_threshold:
                            # Sample diff against current branch
                            diff_proc = subprocess.run(
                                ["git", "diff", f"HEAD...{branch_name}", "--stat"],
                                cwd=repo_path,
                                capture_output=True,
                                text=True,
                                check=False
                            )
                            sample_diff = diff_proc.stdout[:500] if diff_proc.returncode == 0 else ""

                            safe_id = "branch-" + re.sub(r"[^a-zA-Z0-9_-]", "-", branch_name)
                            artifacts.append(
                                DeceasedArtifact(
                                    id=safe_id,
                                    name=branch_name,
                                    artifact_type="BRANCH",
                                    author=author,
                                    last_commit_hash=commit_hash[:8],
                                    last_commit_date=date_str,
                                    last_commit_message=message,
                                    days_dead=days_dead,
                                    cause_of_death=f"Stagnation: abandoned {days_dead} days ago in purgatory",
                                    commits_count=1,
                                    sample_diff=sample_diff
                                )
                            )
    except Exception:
        pass

    # 2. Inspect Stashes
    try:
        stash_proc = subprocess.run(
            ["git", "stash", "list", "--pretty=format:%gd|%aI|%s"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )

        if stash_proc.returncode == 0 and stash_proc.stdout.strip():
            for line in stash_proc.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                parts = line.strip().split("|", 2)
                if len(parts) == 3:
                    stash_ref, date_str, message = parts
                    stash_dt = _parse_iso_date(date_str)
                    days_dead = max(0, (reference_date - stash_dt).days)

                    if days_dead >= stale_days_threshold:
                        safe_id = "stash-" + re.sub(r"[^a-zA-Z0-9_-]", "-", stash_ref)
                        artifacts.append(
                            DeceasedArtifact(
                                id=safe_id,
                                name=stash_ref,
                                artifact_type="STASH",
                                author="Current Developer",
                                last_commit_hash="stash-ref",
                                last_commit_date=date_str,
                                last_commit_message=message,
                                days_dead=days_dead,
                                cause_of_death="Forgotten stash left behind during branch context switch",
                                commits_count=1,
                                sample_diff=""
                            )
                        )
    except Exception:
        pass

    return artifacts
