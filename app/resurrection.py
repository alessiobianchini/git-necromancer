"""Resurrection and Memorial (OFRENDA) engine: reclaims or lays dead code to rest."""

import os
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any
from app.cemetery import DeceasedArtifact

PROTECTED_BRANCHES = {"main", "master", "HEAD", "origin/main", "origin/master"}


def generate_resurrection_patch(repo_path: str, branch_or_stash: str) -> Dict[str, Any]:
    """Generate a clean unified diff patch to resurrect an abandoned branch or stash onto current HEAD."""
    clean_target = branch_or_stash.strip().lstrip("* ")
    if clean_target.lower() in PROTECTED_BRANCHES:
        raise ValueError(f"Cannot resurrect protected branch: {clean_target}")

    # Determine command based on whether target is a stash or a branch
    if clean_target.startswith("stash@{"):
        cmd = ["git", "stash", "show", "-p", clean_target]
    else:
        cmd = ["git", "diff", f"HEAD...{clean_target}"]

    proc = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=False
    )

    patch_content = proc.stdout if proc.returncode == 0 else ""
    files_changed = patch_content.count("diff --git")

    return {
        "success": proc.returncode == 0 and bool(patch_content.strip()),
        "target": clean_target,
        "patch": patch_content,
        "files_changed": files_changed,
        "instructions": (
            f"# To resurrect {clean_target} onto your current branch:\n"
            f"git checkout -b resurrect/{clean_target.replace('/', '-')}\n"
            f"# Save patch to resurrection.patch and run:\n"
            f"git apply resurrection.patch\n"
        )
    }


def grant_final_rites(
    repo_path: str,
    artifact: DeceasedArtifact,
    epitaph: str,
    memorial_file: str = "OFRENDA.md",
    delete_branch: bool = False
) -> Dict[str, Any]:
    """Provide final rites: record an honored memorial tombstone in OFRENDA.md and optionally prune branch."""
    clean_target = artifact.name.strip().lstrip("* ")
    if clean_target.lower() in PROTECTED_BRANCHES:
        raise ValueError(f"Cannot exorcise protected branch: {clean_target}")

    memorial_path = os.path.join(repo_path, memorial_file) if not os.path.isabs(memorial_file) else memorial_file

    tombstone_art = f"""
```plaintext
    .--------------------------------------------------.
   /            +       R.I.P       +                   \\
  |                                                      |
  |  Artifact: {clean_target[:38]:<38}  |
  |  Creator : {artifact.author[:38]:<38}  |
  |  Purgatory: {artifact.days_dead:>3} days in the repo cemetery         |
  |                                                      |
   \\____________________________________________________/
```
"""

    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    memorial_entry = f"""
## 🪦 Rest In Peace: `{clean_target}`
{tombstone_art}

> *"{epitaph}"*

- **Artifact Type**: `{artifact.artifact_type}`
- **Original Creator**: {artifact.author}
- **Final Commit**: `{artifact.last_commit_hash}` — *"{artifact.last_commit_message}"*
- **Final Rites Concluded**: {now_str}

---
"""

    # Ensure header exists if file is new
    needs_header = not os.path.exists(memorial_path) or os.path.getsize(memorial_path) == 0

    with open(memorial_path, "a", encoding="utf-8") as f:
        if needs_header:
            f.write("# 🕯️ The Git Ofrenda: Memorial of Departed Code\n\n")
            f.write("> *\"Here lie the branches and stashes that once burned bright, now laid to rest in eternal peace.\"*\n\n---\n")
        f.write(memorial_entry)

    branch_deleted = False
    if delete_branch:
        if artifact.artifact_type == "STASH":
            del_proc = subprocess.run(
                ["git", "stash", "drop", clean_target],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            branch_deleted = del_proc.returncode == 0
        else:
            del_proc = subprocess.run(
                ["git", "branch", "-D", clean_target],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=False
            )
            branch_deleted = del_proc.returncode == 0

    return {
        "success": True,
        "memorial_path": memorial_path,
        "branch_deleted": branch_deleted,
        "target": clean_target
    }
