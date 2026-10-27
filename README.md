# GitNecromancer (💀🔮)

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](https://opensource.org/licenses/MIT)
[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest%202026-Ghost%20in%20the%20Machine-ff6b6b.svg)](https://dev.to/challenges/hacktoberfest-week4-2026-10-26)
[![Gemma 2 2B](https://img.shields.io/badge/Model-Gemma%202%202B-4285F4.svg)](https://ollama.com/library/gemma2)
[![Render Deploy](https://img.shields.io/badge/Deploy-Render-46E3B7.svg)](https://render.com)
[![Sentry Agent Tracing](https://img.shields.io/badge/Sentry-Agent%20Tracing-362D59.svg)](https://sentry.io)

> **The Open-Source Séance Engine for Dead Code, Abandoned Branches, and Repo Graveyards.**  
> Built for the **Hacktoberfest 2026 Open-Source AI Challenge Week 4: "Ghost in the Machine"**.

🔮 **Live Cloud Demo**: [https://git-necromancer.onrender.com](https://git-necromancer.onrender.com)

---

## 🪦 The Problem: Every Repo is a Cemetery

Behind every active `main` branch lies an eerie underworld of forgotten artifacts:
- Feature branches abandoned 9 months ago after a refactor (`feat/oauth2-rewrite`).
- Experimental spikes that died in merge conflicts (`experiment/vector-search`).
- Ghostly stashes forgotten since a frantic production hotfix (`stash@{0}: WIP on bugfix`).

Developers rarely clean these up because of a primal fear: *"What if there's vital logic or context hidden in that branch?"*

**GitNecromancer (💀🔮)** solves this by turning repo maintenance into an atmospheric, gothic séance powered by **Google Gemma 2 2B** (offline via Ollama), **Sentry Agent Tracing**, **ElevenLabs** eerie voice synthesis, and **Render**.

---

## ✨ Features

- **🔍 Graveyard Surveyor**: Safely scans git history for dead branches (stale >30/90 days, unmerged) and forgotten stashes without mutating your repository.
- **🕯️ AI Code Séance**: Channels the spirit of the deceased code using local **Gemma 2 2B**. The ghost speaks in the first person—explaining who created it, what hopeful mission it had, and the tragic bug or priority shift that killed it.
- **🔊 Spectral Whisper (ElevenLabs)**: Optional atmospheric text-to-speech audio that whispers the ghost's confessions.
- **⚡ Resurrection Ritual**: Reconciles the ancient diff against current `HEAD` and outputs a clean unified patch ready for `git apply`.
- **🪦 The Git Ofrenda**: Grants final rites to branches that deserve peace. Generates a commemorative ASCII tombstone in `OFRENDA.md` and safely purges the branch from git memory.
- **🦇 The Git Catacombs (Web Dashboard)**: A dark gothic web interface built with FastAPI & Tailwind for visual cemetery exploration and audio playback.
- **🛡️ 100% Offline & Private**: Runs locally with Ollama. Zero code ever leaves your machine.

---

## 🚀 Quickstart

### 1. Installation

```bash
git clone https://github.com/alessiobianchini/git-necromancer.git
cd git-necromancer
pip install -r requirements.txt
```

### 2. Environment Configuration (Optional)

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

To run local séances with Gemma 2 2B:
```bash
ollama run gemma2:2b
```

### 3. CLI Commands

```bash
# Survey your repository's dead branches and stashes
python cli.py scan

# Survey the simulated demo graveyard
python cli.py scan --demo

# Summon the spirit of an abandoned branch
python cli.py seance feat/graphql-migration --demo

# Forge a resurrection patch
python cli.py resurrect feat/graphql-migration -o resurrection.patch

# Grant final rites and record in OFRENDA.md
python cli.py exorcise feat/graphql-migration --delete

# Launch The Git Catacombs web dashboard
python cli.py web --port 8000
```

---

## 🌐 The Git Catacombs Web Dashboard

Start the web dashboard:
```bash
python cli.py web
```
Then open `http://localhost:8000` in your browser. You can:
1. Browse graveyard cards showing days dead and cause of death.
2. Click **"Summon Spirit"** to trigger a séance with Gemma 2 2B and listen to the ghost audio.
3. Visit `/ofrenda` to view the memorial altar for departed code.

---

## ☁️ Deploy on Render

Deploy with one click using the included `render.yaml` blueprint:

1. Push your repository to GitHub.
2. In Render, select **Blueprints** and choose `render.yaml`.
3. Render will deploy the web dashboard with full demo mode enabled!

---

## 🧪 Testing

GitNecromancer comes with a complete test suite:

```bash
pytest
```
All 29 tests pass covering cemetery discovery, Sentry tracing, Gemma prompt parsing, ElevenLabs audio caching, patch generation, and FastAPI endpoints.

---

## 📜 License

MIT License. Crafted with 💀 by [Alessio Bianchini](https://github.com/alessiobianchini).
