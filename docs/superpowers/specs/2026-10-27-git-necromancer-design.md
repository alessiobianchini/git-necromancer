# GitNecromancer (💀🔮) Design Specification

> **Theme**: Hacktoberfest 2026 Week 4: "Ghost in the Machine"  
> **Status**: Approved  
> **Date**: 2026-10-27  
> **Author**: Alessio Bianchini <alessio.bianchini@doit.it>

---

## 1. Vision & Core Philosophy

Every software repository is a cemetery.

Behind every active `main` branch lies an eerie underworld of forgotten artifacts:
- Feature branches abandoned 9 months ago after a refactor (`feat/oauth2-rewrite`).
- Experimental spikes that died in merge conflicts (`experiment/vector-search`).
- Ghostly stashes forgotten since a frantic production hotfix (`stash@{0}: WIP on bugfix`).
- Legacy modules that were silently commented out or deprecated without closure.

Developers rarely clean these up because of a primal fear: *"What if there's a vital piece of logic or context hidden in that branch?"*

**GitNecromancer (💀🔮)** solves this by turning repo maintenance into an atmospheric, gothic séance powered by **Google Gemma 2 2B** (offline via Ollama), **Sentry Agent Tracing**, **ElevenLabs** eerie voice synthesis, and **Render**.

Instead of a dry `git branch -D`, GitNecromancer allows developers to:
1. **Survey the Graveyard**: Scan local repositories for deceased branches (stale >30/90 days, unmerged), orphaned stashes, and dead code.
2. **Hold a Séance**: Summon the spirit of the deceased code. Using local Gemma 2, the ghost speaks in the first person—explaining who created it, what hopeful mission it had, and the tragic bug or priority shift that killed it.
3. **Listen to the Ghost (ElevenLabs)**: Hear the spirit speak with an eerie gothic whisper generated via TTS.
4. **Choose its Fate**:
   - **Resurrect**: Reconcile the ancient diff against current `main` and output a clean resurrection patch or new PR.
   - **Exorcise & Memorialize (Git Ofrenda)**: Provide the code with final rites. GitNecromancer writes an honoring epitaph to `OFRENDA.md` (or `MEMORIAL.md`) with an ASCII tombstone, records its commits, and safely purges the branch.

---

## 2. Multi-Category Sponsor Alignment

GitNecromancer is architected specifically to sweep the Hacktoberfest Week 4 prize pool:

| Category | Target Prize | Integration Details |
|---|---|---|
| **Overall Week 4 Winner** | **$250** | Perfect marriage of the Halloween "Ghost in the Machine" theme with real developer utility, dark gothic aesthetics, and humor. |
| **Best Use of Gemma** | **$200** | 100% offline, local inference via `gemma2:2b` using Ollama. High creative fidelity for first-person ghostly monologues and precise technical reasoning for patch reconstruction. $0 cost, zero data leakage. |
| **Best Use of Render** | **$200** | Full web dashboard ("The Git Catacombs") deployable via `render.yaml`. Includes interactive cemetery viewer, audio séance playback, and mock demo mode for judges without local repos. |
| **Best Use of Sentry Agent Tracing** | **$100** | OpenTelemetry AI tracing instrumenting every séance invocation: span latencies, prompt/completion tokens, model temperature, and ritual status. |
| **Best Use of ElevenLabs** | **$100** | Atmospheric, ghostly voice synthesis rendering the Gemma-generated spectral confessions as streaming audio. |

---

## 3. Architecture & Components

```
git-necromancer/
├── pyproject.toml              # Modern Python build config
├── requirements.txt            # Core dependencies (fastapi, uvicorn, jinja2, rich, requests, sentry-sdk)
├── render.yaml                 # One-click Render cloud deployment blueprint
├── cli.py                      # Utilitarian, gothic CLI entrypoint
├── app/
│   ├── __init__.py
│   ├── config.py               # Settings (repo paths, Ollama URL, Sentry DSN, ElevenLabs key)
│   ├── cemetery.py             # Git cemetery surveyor (branches, stashes, commit churn)
│   ├── seance.py               # Gemma 2 2B prompt engineering & Ollama client
│   ├── resurrection.py         # Patch synthesis & OFRENDA.md memorial generator
│   ├── voice.py                # ElevenLabs voice generation & local caching
│   ├── telemetry.py            # Sentry agent tracing & OpenTelemetry spans
│   └── web/
│       ├── __init__.py
│       ├── server.py           # FastAPI application
│       ├── templates/          # Gothic dark-mode HTML templates (Jinja2)
│       └── static/             # Gothic CSS, spooky sound effects, and animations
├── tests/
│   ├── test_cemetery.py        # Tests for dead branch and stash detection
│   ├── test_seance.py          # Tests for ghost prompt construction & Ollama response parsing
│   ├── test_resurrection.py    # Tests for diff creation and OFRENDA generation
│   ├── test_voice.py           # Tests for ElevenLabs TTS and fallback behavior
│   └── test_telemetry.py      # Tests for Sentry span instrumentation
└── docs/
    └── superpowers/            # Specs and implementation plans
```

---

## 4. Key Subsystem Specifications

### 4.1 Cemetery Scanner (`app/cemetery.py`)
- Executes safe native git commands:
  - `git branch --no-merged main`
  - `git log -1 --format=%H|%aI|%an|%s <branch>`
  - `git stash list --pretty=format:%gd|%aI|%gs`
- Metrics calculated per deceased artifact:
  - **Days Dead**: Days since the last commit on the branch or stash.
  - **Cause of Death**: Stagnation (>90 days), Divergence (>20 commits behind `main`), or Merge Conflict.
  - **Artifact Type**: `BRANCH`, `STASH`, or `ZOMBIE_CODE`.
- Provides mock graveyard data when running in cloud environments (e.g. Render) without local git access.

### 4.2 Séance Engine (`app/seance.py`)
- Connects to local `http://localhost:11434/api/generate` running `gemma2:2b`.
- Prompts engineered for authentic personality:
  - The AI speaks as the spirit of the code itself.
  - Highlights specific files, commit messages, and the tragic reason it was abandoned.
  - Keeps it witty, evocative, and technically accurate.
- Fallback heuristic generator if Ollama is unreachable, ensuring 100% uptime for online demos.

### 4.3 Resurrection & Memorial Engine (`app/resurrection.py`)
- **Resurrect**:
  - Computes `git diff main...<branch>` or extracts stash diffs.
  - Gemma 2 identifies conflicts and generates a patch ready for application via `git apply`.
- **Exorcise & Memorialize**:
  - Generates an entry in `OFRENDA.md` with:
    - ASCII Art tombstone with the branch name and lifespan dates.
    - Epitaph written by the code spirit.
    - List of key commits and contributors.
  - Safe branch deletion (`git branch -d` or `-D` only with explicit confirmation).

### 4.4 Gothic Web Dashboard ("The Git Catacombs")
- Dark obsidian and purple palette (`#0d0c13`, `#1a162b`, `#8b5cf6`, `#ec4899`).
- Interactive Graveyard Table:
  - Tombstones representing dead branches with "Days in Purgatory".
  - One-click **"Summon Ghost"** button with eerie audio playback.
  - Action buttons: **"Resurrect (Copy Patch)"** and **"Grant Peace (Add to Memorial)"**.
- Virtual Ofrenda tab displaying all honored code souls.

---

## 5. Security & Privacy Guarantees
- 100% local inference: Code contents and commit messages never leave the developer's workstation.
- Read-only by default: Git inspection never mutates repository state unless the user explicitly requests an exorcism or patch application.
- API keys (ElevenLabs, Sentry) are optional and read from `.env` or system environment.
