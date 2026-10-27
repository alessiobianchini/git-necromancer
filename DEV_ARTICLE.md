---
title: "GitNecromancer: The Open-Source Séance Engine for Dead Code and Repo Graveyards"
published: false
description: "Turn abandoned branches into speaking code ghosts with local Gemma 2 2B, Sentry Agent Tracing, ElevenLabs, and Render."
tags: devchallenge, hf26challenge, gemma, render, sentry
cover_image: ""
canonical_url: ""
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 4: Ghost in the Machine](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)*

---

## What I Built

Every software repository is secretly a graveyard.

Behind every polished `main` branch lies an eerie catacomb of departed code:
* The ambitious feature branch abandoned 8 months ago during an architecture debate (`feat/graphql-migration`).
* The frantic midnight spike that fixed an outage but was never cleaned up (`stash@{0}: WIP on hotfix`).
* The experimental caching layer that stalled when someone left the company (`experiment/redis-layer`).

As developers, we carry a collective guilt. We look at our branch list, shudder, and whisper: *"I really should clean those up..."* 

Yet, we never do. Why? Because of a primal fear: **what if there is a vital piece of context or logic trapped inside that dead branch?** Running a blind `git branch -D` feels like desecrating a tomb without knowing who was buried there.

So for the final week of Hacktoberfest 2026 (*Ghost in the Machine*), I built **GitNecromancer (💀🔮)**: an atmospheric open-source developer tool and gothic web dashboard that turns repository cleanup into a supernatural séance powered by **Google Gemma 2 2B** running locally via **Ollama**, **Sentry Agent Tracing**, **ElevenLabs** eerie audio synthesis, and **Render**.

Instead of staring at stale git logs, GitNecromancer allows you to:
1. **Survey the Graveyard**: Safely inspect unmerged branches, orphaned stashes, and commit stagnation across your repositories.
2. **Conduct an AI Séance**: Summon the spirit of any deceased code artifact. Using **Gemma 2 2B**, the ghost speaks in the first person—confessing who created it, what hopeful mission it had, and the tragic conflict or priority shift that killed it.
3. **Listen to the Ghost Whisper**: Hear the spirit speak through eerie atmospheric voice synthesis generated via **ElevenLabs**.
4. **Choose Its Eternal Fate**:
   - **⚡ Reincarnate (Resurrect)**: Gemma analyzes the ancient diff against current `HEAD` and generates a clean unified patch ready for `git apply`.
   - **🪦 Grant Final Rites (The Git Ofrenda)**: Provide the code with honorable closure. GitNecromancer writes a commemorative ASCII tombstone into `OFRENDA.md` and safely purges the branch from git memory.

---

## Demo

You can experience the live interactive dashboard immediately without installing anything:  
👉 **[https://git-necromancer.onrender.com](https://git-necromancer.onrender.com)**

GitNecromancer operates both as an obsidian-dark web dashboard called **"The Git Catacombs"** and a rich terminal CLI.

### 1. The Terminal Séance

Running `python cli.py scan` surveys the local graveyard:

```plaintext
   .---.       GitNecromancer (💀🔮)
  /     \      The Open-Source Séance Engine for Dead Code
 | () () |     Hacktoberfest 2026: Ghost in the Machine
  \  ^  /
   |||||

🔍 Surveying repo graveyard at: . ...

                 🪦 Repository Graveyard (Restless Code Souls)                 
┌──────────┬──────────────────────┬─────────────┬───────────┬──────────────────────────────────────────┐
│ Type     │ Artifact / Branch    │ Creator     │ Purgatory │ Cause of Death                           │
├──────────┼──────────────────────┼─────────────┼───────────┼──────────────────────────────────────────┤
│ BRANCH   │ feat/graphql-migr... │ Devon Vance │  255 days │ Architecture churn: team decided REST    │
│ BRANCH   │ experiment/redis-... │ Sarah Connor│  207 days │ Memory leak in staging: rolled back      │
│ STASH    │ stash@{0}            │ Alessio B.  │  161 days │ Interrupted hotfix: developer switched   │
└──────────┴──────────────────────┴─────────────┴───────────┴──────────────────────────────────────────┘
```

When you channel a spirit with `python cli.py seance feat/graphql-migration`:

```plaintext
🕯️ Lighting candles for: feat/graphql-migration
Summoning local spirit via Gemma 2 2B (Ollama)...

┌──────────────────── 👻 Spirit of feat/graphql-migration ────────────────────┐
│ "I was summoned into existence 255 days ago by Devon Vance. I still recall  │
│ the frantic keystrokes of 'WIP: switch users endpoint to GraphQL schema' in │
│ feat/graphql-migration. Alas, priorities shifted like mist in the night,    │
│ and my branch was left to wither in the cold purgatory of git history."     │
│                                                                             │
│ 🔍 Autopsy: The pull request was never opened; context switching and        │
│ architectural drift doomed feat/graphql-migration.                          │
│ 🔮 Suggested Fate: MEMORIALIZE (Difficulty: MEDIUM)                         │
│ ⚡ Model: gemma2:2b (local) | Tokens: 110 | Traced via Sentry Agent Tracing │
└─────────────────────────────────────────────────────────────────────────────┘

Ritual choices:
  - Resurrect: python cli.py resurrect feat/graphql-migration
  - Grant Peace: python cli.py exorcise feat/graphql-migration --delete
```

### 2. The Git Catacombs (Web Dashboard)

Launching `python cli.py web` opens the gothic dashboard on port 8000:
- **Graveyard Cards**: Displays time in purgatory, creator, and last commit preview.
- **Interactive Séance Modal**: Features a flickering candle animation, streaming monologue, and an audio player for ElevenLabs ghost whispering.
- **One-Click Patch & Ofrenda**: Copy resurrection patches or grant final rites with instant DOM updates.

---

## Code

{% github alessiobianchini/git-necromancer %}

The entire codebase is open-source and hosted on GitHub:  
👉 **[https://github.com/alessiobianchini/git-necromancer](https://github.com/alessiobianchini/git-necromancer)**

---

## How I Built It

GitNecromancer was engineered with a strict **anti-bloat, local-first** architecture:

```
git-necromancer/
├── cli.py               # Utilitarian, gothic Rich terminal CLI
├── render.yaml          # Zero-config Render cloud blueprint
├── app/
│   ├── config.py        # Settings & environment autodetection
│   ├── cemetery.py      # Git cemetery scanner (branches, stashes, churn)
│   ├── seance.py        # Gemma 2 2B prompt engineering & Ollama client
│   ├── resurrection.py  # Patch synthesis & OFRENDA.md memorial generator
│   ├── voice.py         # ElevenLabs audio generation & disk caching
│   ├── telemetry.py     # Sentry OpenTelemetry agent tracing
│   └── web/             # FastAPI gothic web dashboard & Jinja2 templates
└── tests/               # 29/29 passing unit & integration tests
```

### 1. Local Open-Weight AI with Google Gemma 2 2B
Code privacy is non-negotiable. Developers cannot paste proprietary codebases and internal commit messages into public cloud APIs just to clean up dead branches.

GitNecromancer uses **Google Gemma 2 2B** running 100% offline via **Ollama**. Gemma 2 2B proved to be the ideal open-weight model for this challenge:
- **Lightweight footprint**: Runs comfortably on consumer laptops and developer machines with less than 2GB of VRAM.
- **Creative voice & persona**: When prompted with git metadata (author, branch name, commit message, time in purgatory, diff snippet), Gemma adopts a gothic, atmospheric first-person persona while maintaining razor-sharp technical diagnostic accuracy.
- **Zero cloud leaks & $0.00 cost**: All inference happens on `localhost:11434`.

### 2. Sentry Agent Tracing & OpenTelemetry Instrumentation
Every spiritual invocation is observed through **Sentry Agent Tracing**:
- Using OpenTelemetry spans (`gen_ai.chat`, `seance:summon`), GitNecromancer captures prompt and completion token counts, latency profiles, and model configurations.
- Spans record whether the séance channeled a local Ollama model or utilized the built-in spectral heuristic fallback.
- If Sentry is not configured, the telemetry module acts as a transparent, zero-overhead no-op.

### 3. Ghost Voice Synthesis via ElevenLabs
To make the séance truly unforgettable, GitNecromancer integrates with **ElevenLabs**:
- The first-person monologue generated by Gemma is transformed into an eerie, whispering audio confession.
- Audio outputs are deterministically hashed and cached on disk (`audio_cache/`) to eliminate duplicate API requests and conserve credits.
- If no API key is provided, the system gracefully degrades to text-only mode without warnings.

### 4. Deployable on Render ("The Git Catacombs")
To allow developers and judges to experience GitNecromancer immediately without installing Ollama locally, the web dashboard is packaged with a `render.yaml` blueprint:
- Runs FastAPI + Uvicorn on Python 3.11+.
- Includes an automatic **Demo Graveyard** containing realistic abandoned branches (`feat/graphql-migration`, `experiment/redis-layer`, `stash@{0}`) so anyone can hold séances in the cloud.

### 5. Honorable Final Rites: The Git Ofrenda
In Mexican culture, *Día de los Muertos* celebrates departed souls rather than fearing them. 

GitNecromancer embraces this through **The Git Ofrenda**: when you grant peace to an abandoned branch (`python cli.py exorcise <branch> --delete`), it carves an ASCII headstone into `OFRENDA.md`, recording the branch name, creator, and epitaph before safely deleting the branch. You keep the memory and lessons learned forever without cluttering your git graph.

---

## Why Open Innovation Matters

The "Ghost in the Machine" theme is often treated as a spooky trope, but in software engineering, ghosts are very real: they are the legacy code, forgotten architectural decisions, and abandoned branches that haunt our repositories.

This project demonstrated why **open-weight models like Gemma 2** are essential for the future of software development:
1. **Privacy**: Proprietary repositories contain corporate trade secrets and intellectual property. Open-weight models allow developers to build AI-assisted tools that run entirely air-gapped on developer workstations.
2. **Affordability**: Building local developer utilities shouldn't require monthly SaaS subscriptions or token metering. A local Gemma 2 2B model costs $0.00 to run for a million séances.
3. **Hackability & Joy**: Open tooling allows us to take serious technical problems—like branch drift, merge debt, and repository rot—and turn them into creative, joyful, and memorable experiences.

Clean your repo cemeteries, honor your fallen code, and happy Hacktoberfest! 🪦🕯️

---
*Built with 💀 by [Alessio Bianchini](https://github.com/alessiobianchini). Let me know in the comments: what is the oldest dead branch haunting your repository right now?*
