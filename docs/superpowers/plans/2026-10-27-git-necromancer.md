# GitNecromancer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build GitNecromancer (💀🔮), a gothic developer tool and web dashboard powered by local Gemma 2 2B, Sentry Agent Tracing, ElevenLabs, and Render to scan repo graveyards for dead branches/stashes, summon speaking code ghosts, and either resurrect or memorialize them with final rites.

**Architecture:** A modular Python engine with native Git inspection (`cemetery.py`), local Ollama Gemma 2 2B prompt orchestration (`seance.py`), Sentry OpenTelemetry span tracing (`telemetry.py`), ElevenLabs spooky audio synthesis (`voice.py`), patch & `OFRENDA.md` memorial generator (`resurrection.py`), backed by both an interactive Rich terminal CLI (`cli.py`) and a dark gothic FastAPI dashboard (`app/web`).

**Tech Stack:** Python 3.11+, FastAPI, Uvicorn, Jinja2, Rich, Requests, Sentry-SDK, Ollama (Gemma 2 2B), Pytest, Render.

**Spec:** `docs/superpowers/specs/2026-10-27-git-necromancer-design.md`

## Global Constraints
- Commit author: `--author="Alessio Bianchini <alessio.bianchini@doit.it>"`
- All code, comments, docstrings, variable names, CLI output, and web copy in English.
- Privacy & Local First: 100% offline inference capability with graceful offline/mock fallback for cloud demos.
- High aesthetic standard: gothic, atmospheric, witty, respectful of developer time.

## Review Focus
1. Repositories with no dead branches: Cemetery scanner must return an empty graveyard status without error.
2. Ollama service unavailable: Séance engine must provide an evocative heuristic fallback and mark status in telemetry.
3. ElevenLabs API key missing: Voice engine must gracefully degrade to text-only without throwing exceptions.
4. Protected branches: Never allow accidental exorcism (deletion) of `main`, `master`, or current active branch.
5. Sentry disabled/misconfigured: Telemetry wrappers must operate as transparent no-ops when Sentry DSN is not provided.

---

### Task 1: Project Scaffolding & Git Init & Core Configuration
**Files:**
- Create: `pyproject.toml`
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `app/__init__.py`
- Create: `app/config.py`
- Test: `tests/test_config.py`

- [ ] Initialize git repository at `D:\Git\Ale\git-necromancer`.
- [ ] Configure `requirements.txt` with `fastapi`, `uvicorn`, `jinja2`, `rich`, `requests`, `sentry-sdk`, `pytest`.
- [ ] Write `app/config.py` using `pydantic-settings` or simple `dataclass` loading environment variables.
- [ ] Write `tests/test_config.py` validating default settings and environment override.
- [ ] Run pytest to verify configuration loading.
- [ ] Commit changes.

---

### Task 2: Git Cemetery Scanner
**Files:**
- Create: `app/cemetery.py`
- Test: `tests/test_cemetery.py`

- [ ] Write failing test in `tests/test_cemetery.py` verifying detection of stale unmerged branches, stashes, and commit age.
- [ ] Implement `app/cemetery.py` with `scan_graveyard(repo_path)` returning `DeceasedArtifact` objects.
- [ ] Add mock graveyard generator for cloud demo mode when no git repo is present.
- [ ] Run tests and verify all pass.
- [ ] Commit changes.

---

### Task 3: Sentry Agent Tracing & Telemetry
**Files:**
- Create: `app/telemetry.py`
- Test: `tests/test_telemetry.py`

- [ ] Write failing test in `tests/test_telemetry.py` checking span lifecycle, token metrics recording, and no-op safety.
- [ ] Implement `app/telemetry.py` providing `trace_seance(artifact_id)` and `record_token_usage(...)`.
- [ ] Run tests and verify all pass.
- [ ] Commit changes.

---

### Task 4: Gemma 2 2B Séance AI Engine
**Files:**
- Create: `app/seance.py`
- Test: `tests/test_seance.py`

- [ ] Write failing test in `tests/test_seance.py` verifying prompt template structure, Ollama response parsing, and heuristic fallback.
- [ ] Implement `app/seance.py` with `conduct_seance(artifact, model="gemma2:2b")` generating first-person ghost confessions and autopsy reports.
- [ ] Integrate with `telemetry.py` to trace séance duration and token counts.
- [ ] Run tests and verify all pass.
- [ ] Commit changes.

---

### Task 5: ElevenLabs Ghost Voice Engine
**Files:**
- Create: `app/voice.py`
- Test: `tests/test_voice.py`

- [ ] Write failing test in `tests/test_voice.py` testing audio synthesis request mocking, file caching, and fallback behavior.
- [ ] Implement `app/voice.py` with `synthesize_ghost_voice(text, voice_id="shadow")` returning audio path or bytes.
- [ ] Run tests and verify all pass.
- [ ] Commit changes.

---

### Task 6: Resurrection & Memorial (OFRENDA) Engine
**Files:**
- Create: `app/resurrection.py`
- Test: `tests/test_resurrection.py`

- [ ] Write failing test in `tests/test_resurrection.py` verifying patch generation and `OFRENDA.md` markdown formatting with ASCII tombstone.
- [ ] Implement `generate_resurrection_patch(repo_path, branch)` and `grant_final_rites(repo_path, branch, epitaph)`.
- [ ] Add safety check protecting `main`, `master`, and `HEAD`.
- [ ] Run tests and verify all pass.
- [ ] Commit changes.

---

### Task 7: Gothic CLI Experience
**Files:**
- Create: `cli.py`
- Test: `tests/test_cli.py`

- [ ] Implement Rich terminal UI with candle flicker effect, cemetery table, and interactive menu (`scan`, `seance`, `resurrect`, `exorcise`).
- [ ] Write test in `tests/test_cli.py` checking CLI argument parsing and commands.
- [ ] Run tests and verify all pass.
- [ ] Commit changes.

---

### Task 8: Gothic Web Dashboard ("The Git Catacombs")
**Files:**
- Create: `app/web/server.py`
- Create: `app/web/templates/base.html`
- Create: `app/web/templates/index.html`
- Create: `app/web/templates/ofrenda.html`
- Create: `app/web/static/gothic.css`
- Test: `tests/test_web.py`

- [ ] Build FastAPI server with endpoints: `/`, `/api/graveyard`, `/api/seance`, `/api/resurrect`, `/api/exorcise`, `/api/audio/{artifact_id}`.
- [ ] Create dark obsidian/purple responsive UI with tombstone cards, audio player, and virtual ofrenda.
- [ ] Write test in `tests/test_web.py` using `TestClient` to verify all endpoints return 200 OK.
- [ ] Run tests and verify all pass.
- [ ] Commit changes.

---

### Task 9: Render Blueprint (`render.yaml`) & Verification
**Files:**
- Create: `render.yaml`
- Create: `Dockerfile` (or native Python web service specification)

- [ ] Define `render.yaml` with Python 3 web service, build command, start command `uvicorn app.web.server:app --host 0.0.0.0 --port $PORT`.
- [ ] Verify local execution on port 8000.
- [ ] Commit changes.

---

### Task 10: DEV Article Draft for Hacktoberfest Week 4
**Files:**
- Create: `DEV_ARTICLE.md`

- [ ] Draft full article following the official Week 4 template:
  - Header with `tags: devchallenge, hf26challenge, gemma, render, sentry`
  - "What I Built", "Demo", "Code", "How I Built It" (Gemma, Sentry, Render, ElevenLabs), "Why Open Innovation Matters".
- [ ] Review against DEV rules and ensure tone is human, engaging, and authoritative.
- [ ] Commit final article.
