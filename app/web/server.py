"""FastAPI web server for GitNecromancer: The Git Catacombs."""

import os
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.cemetery import scan_graveyard, get_mock_graveyard, DeceasedArtifact
from app.config import get_settings
from app.resurrection import generate_resurrection_patch, grant_final_rites
from app.seance import conduct_seance, SeanceResult
from app.telemetry import init_telemetry
from app.voice import synthesize_ghost_voice

# Initialize app and configuration
settings = get_settings()
init_telemetry(settings.SENTRY_DSN, settings.SENTRY_ENVIRONMENT)

app = FastAPI(
    title="GitNecromancer",
    description="The Open-Source Séance Engine for Dead Code, Abandoned Branches, and Repo Graveyards",
    version="0.1.0"
)

# Resolve paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs("audio_cache", exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


class ExorciseRequest(BaseModel):
    target: str
    epitaph: str = "Laid to rest with eternal honor."
    delete_branch: bool = False


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """Render the main Git Catacombs dashboard."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/ofrenda", response_class=HTMLResponse)
async def get_ofrenda(request: Request):
    """Render the Git Ofrenda memorial wall."""
    ofrenda_path = os.path.join(settings.REPO_PATH, "OFRENDA.md")
    content = ""
    if os.path.exists(ofrenda_path):
        with open(ofrenda_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = (
            "# 🕯️ The Git Ofrenda: Memorial of Departed Code\n\n"
            "> *\"No souls have been laid to rest in this ofrenda yet.*\"\n\n"
            "Channel an abandoned branch in the Catacombs and grant it final rites to erect its tombstone here."
        )
    return templates.TemplateResponse(
        request=request,
        name="ofrenda.html",
        context={"ofrenda_content": content}
    )


@app.get("/api/graveyard")
async def api_graveyard(demo: bool = False):
    """List deceased artifacts in repository or return demo mock graveyard."""
    if demo:
        return get_mock_graveyard()

    artifacts = scan_graveyard(settings.REPO_PATH)
    if not artifacts:
        # Fallback to mock graveyard if local repo has no dead branches
        return get_mock_graveyard()
    return artifacts


@app.post("/api/seance/{artifact_id}")
async def api_seance(artifact_id: str, demo: bool = False):
    """Conduct a code séance channeled by Gemma 2 2B."""
    # Find artifact in demo list or local scan
    artifacts = get_mock_graveyard() if demo else scan_graveyard(settings.REPO_PATH)
    if not artifacts:
        artifacts = get_mock_graveyard()

    artifact = next((a for a in artifacts if a.id == artifact_id or a.name == artifact_id), None)
    if not artifact:
        # Synthesize ad-hoc artifact
        artifact = DeceasedArtifact(
            id=artifact_id,
            name=artifact_id,
            artifact_type="BRANCH",
            author="Unknown Wanderer",
            last_commit_hash="deadbeef",
            last_commit_date="2024-01-01T00:00:00+00:00",
            last_commit_message="Legacy experiment",
            days_dead=180,
            cause_of_death="Abandoned in purgatory",
            commits_count=1,
            sample_diff=""
        )

    result = conduct_seance(
        artifact=artifact,
        ollama_url=settings.OLLAMA_BASE_URL,
        model=settings.OLLAMA_MODEL
    )

    audio_url = None
    if settings.ELEVENLABS_API_KEY:
        audio_path = synthesize_ghost_voice(
            result.ghost_monologue,
            api_key=settings.ELEVENLABS_API_KEY,
            voice_id=settings.ELEVENLABS_VOICE_ID,
            cache_dir="audio_cache"
        )
        if audio_path:
            filename = os.path.basename(audio_path)
            audio_url = f"/api/audio/{filename}"

    res_dict = result.model_dump()
    res_dict["audio_url"] = audio_url
    return res_dict


@app.post("/api/resurrect/{target:path}")
async def api_resurrect(target: str):
    """Generate resurrection patch for an abandoned branch."""
    try:
        patch_info = generate_resurrection_patch(settings.REPO_PATH, target)
        return patch_info
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/exorcise")
async def api_exorcise(req: ExorciseRequest):
    """Grant final rites, record tombstone in OFRENDA.md and optionally delete branch."""
    artifact = DeceasedArtifact(
        id=f"branch-{req.target.replace('/', '-')}",
        name=req.target,
        artifact_type="BRANCH",
        author="Departed Soul",
        last_commit_hash="deadbeef",
        last_commit_date="2024-01-01T00:00:00+00:00",
        last_commit_message="Farewell",
        days_dead=120,
        cause_of_death="Granted peace by developer",
        commits_count=1,
        sample_diff=""
    )

    res = grant_final_rites(
        repo_path=settings.REPO_PATH,
        artifact=artifact,
        epitaph=req.epitaph,
        memorial_file="OFRENDA.md",
        delete_branch=req.delete_branch
    )
    return res


@app.get("/api/audio/{filename}")
async def api_audio(filename: str):
    """Serve synthesized ghost voice audio file."""
    safe_filename = os.path.basename(filename)
    audio_path = os.path.join("audio_cache", safe_filename)
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio spirit not found")
