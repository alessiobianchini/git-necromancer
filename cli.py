import argparse
import sys

# Force UTF-8 encoding on Windows console for emoji and gothic glyphs
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console(highlight=False)
from app.cemetery import scan_graveyard, get_mock_graveyard, DeceasedArtifact
from app.config import get_settings
from app.resurrection import generate_resurrection_patch, grant_final_rites
from app.seance import conduct_seance
from app.telemetry import init_telemetry
from app.voice import synthesize_ghost_voice

console = Console()

BANNER = """
   .---.       [bold magenta]GitNecromancer (💀🔮)[/bold magenta]
  /     \\      [dim]The Open-Source Séance Engine for Dead Code[/dim]
 | () () |     [italic purple]Hacktoberfest 2026: Ghost in the Machine[/italic purple]
  \\  ^  /
   |||||
"""


def build_parser() -> argparse.ArgumentParser:
    """Build command line argument parser."""
    common_parent = argparse.ArgumentParser(add_help=False)
    common_parent.add_argument("--repo", default=".", help="Path to git repository (default: current directory)")
    common_parent.add_argument("--demo", action="store_true", help="Use mock cemetery data for live demos")

    parser = argparse.ArgumentParser(
        prog="git-necromancer",
        parents=[common_parent],
        description="The Open-Source Séance Engine for Dead Code, Abandoned Branches, and Repo Graveyards"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # scan
    subparsers.add_parser("scan", parents=[common_parent], help="Scan repository cemetery for dead branches and stashes")

    # seance
    seance_parser = subparsers.add_parser("seance", parents=[common_parent], help="Hold a séance to channel the spirit of an abandoned branch")
    seance_parser.add_argument("target", help="Branch name or stash identifier to channel")

    # resurrect
    resurrect_parser = subparsers.add_parser("resurrect", parents=[common_parent], help="Reincarnate abandoned code as a clean patch on current branch")
    resurrect_parser.add_argument("target", help="Branch name or stash identifier to resurrect")
    resurrect_parser.add_argument("-o", "--output", default="resurrection.patch", help="Output patch file name")

    # exorcise
    exorcise_parser = subparsers.add_parser("exorcise", parents=[common_parent], help="Grant final rites, record tombstone in OFRENDA.md and purge branch")
    exorcise_parser.add_argument("target", help="Branch name or stash identifier to lay to rest")
    exorcise_parser.add_argument("--delete", action="store_true", help="Permanently delete the branch from git")

    # web
    web_parser = subparsers.add_parser("web", parents=[common_parent], help="Start the Git Catacombs gothic web dashboard")
    web_parser.add_argument("-p", "--port", type=int, default=8000, help="Web server port (default: 8000)")
    web_parser.add_argument("-H", "--host", default="0.0.0.0", help="Web server host (default: 0.0.0.0)")

    return parser


def handle_scan(repo_path: str, use_demo: bool) -> int:
    """Scan and print the repository cemetery."""
    console.print(BANNER)
    console.print(f"[bold cyan]🔍 Surveying repo graveyard at:[/bold cyan] [yellow]{repo_path}[/yellow]...\n")

    artifacts = get_mock_graveyard() if use_demo else scan_graveyard(repo_path)
    if not artifacts and not use_demo:
        # Check if user wants to see demo data if local repo is clean
        console.print("[green]✨ The cemetery is peaceful. No dead or restless branches found![/green]")
        console.print("[dim](Tip: run with --demo to inspect a simulated repository graveyard)[/dim]\n")
        return 0

    table = Table(title="🪦 Repository Graveyard (Restless Code Souls)", header_style="bold magenta")
    table.add_column("Type", style="cyan", width=8)
    table.add_column("Artifact / Branch", style="bold white")
    table.add_column("Creator", style="green")
    table.add_column("Purgatory", style="bold red", justify="right")
    table.add_column("Cause of Death", style="dim italic")

    for art in artifacts:
        table.add_row(
            art.artifact_type,
            art.name,
            art.author,
            f"{art.days_dead} days",
            art.cause_of_death[:60]
        )

    console.print(table)
    console.print("\n[bold]Next ritual step:[/bold] Run [magenta]python cli.py seance <branch-name>[/magenta] to summon the spirit.\n")
    return 0


def handle_seance(repo_path: str, target: str, use_demo: bool) -> int:
    """Conduct an AI séance for the requested branch."""
    settings = get_settings()
    init_telemetry(settings.SENTRY_DSN, settings.SENTRY_ENVIRONMENT)

    artifacts = get_mock_graveyard() if use_demo else scan_graveyard(repo_path)
    artifact = next((a for a in artifacts if a.name == target or a.id == target), None)

    if not artifact:
        # Create ad-hoc artifact from target name if not found in scanner
        artifact = DeceasedArtifact(
            id=f"branch-{target.replace('/', '-')}",
            name=target,
            artifact_type="BRANCH",
            author="Unknown Wanderer",
            last_commit_hash="deadbeef",
            last_commit_date="2024-01-01T00:00:00+00:00",
            last_commit_message="Legacy changes",
            days_dead=180,
            cause_of_death="Abandoned in purgatory",
            commits_count=1,
            sample_diff=""
        )

    console.print(BANNER)
    console.print(f"[bold magenta]🕯️ Lighting candles for:[/bold magenta] [bold white]{artifact.name}[/bold white]")
    console.print("[italic dim]Summoning local spirit via Gemma 2 2B (Ollama)...[/italic dim]\n")

    seance_res = conduct_seance(artifact, ollama_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL)

    panel_content = Text()
    panel_content.append(f"\"{seance_res.ghost_monologue}\"\n\n", style="bold italic yellow")
    panel_content.append("🔍 Autopsy: ", style="bold red")
    panel_content.append(f"{seance_res.cause_of_death_analysis}\n", style="italic")
    panel_content.append("🔮 Suggested Fate: ", style="bold magenta")
    panel_content.append(f"{seance_res.suggested_action} (Difficulty: {seance_res.resurrection_difficulty})\n", style="bold")
    panel_content.append(f"⚡ Model: {seance_res.model_used} | Tokens: {seance_res.prompt_tokens + seance_res.completion_tokens}", style="dim")

    console.print(Panel(panel_content, title=f"👻 Spirit of {artifact.name}", border_style="magenta"))

    # Synthesize audio if ElevenLabs key is present
    if settings.ELEVENLABS_API_KEY:
        console.print("[italic dim]Synthesizing ghost voice via ElevenLabs...[/italic dim]")
        audio_path = synthesize_ghost_voice(seance_res.ghost_monologue, api_key=settings.ELEVENLABS_API_KEY)
        if audio_path:
            console.print(f"[green]🔊 Ghost audio whispered into:[/green] [white]{audio_path}[/white]")

    console.print("\n[bold]Ritual choices:[/bold]")
    console.print(f"  - Resurrect: [cyan]python cli.py resurrect {artifact.name}[/cyan]")
    console.print(f"  - Grant Peace: [red]python cli.py exorcise {artifact.name} --delete[/red]\n")
    return 0


def handle_resurrect(repo_path: str, target: str, output: str) -> int:
    """Generate resurrection patch."""
    console.print(f"[bold cyan]⚡ Attempting resurrection ritual for:[/bold cyan] [bold white]{target}[/bold white]...")
    try:
        res = generate_resurrection_patch(repo_path, target)
        if res["success"] and res["patch"]:
            with open(output, "w", encoding="utf-8") as f:
                f.write(res["patch"])
            console.print(f"[green]✨ Resurrection patch forged:[/green] [bold yellow]{output}[/bold yellow] ({res['files_changed']} files)")
            console.print(Panel(res["instructions"], title="Resurrection Incantation", border_style="cyan"))
            return 0
        else:
            console.print(f"[yellow]⚠️ No diff found between HEAD and {target}. Code may already be merged![/yellow]")
            return 1
    except Exception as exc:
        console.print(f"[red]❌ Resurrection ritual failed: {exc}[/red]")
        return 1


def handle_exorcise(repo_path: str, target: str, delete_branch: bool) -> int:
    """Provide final rites and add to OFRENDA.md."""
    console.print(f"[bold red]🪦 Administering final rites to:[/bold red] [bold white]{target}[/bold white]...")
    artifact = DeceasedArtifact(
        id=f"branch-{target.replace('/', '-')}",
        name=target,
        artifact_type="BRANCH",
        author="Departed Contributor",
        last_commit_hash="deadbeef",
        last_commit_date="2024-01-01T00:00:00+00:00",
        last_commit_message="Rest in peace",
        days_dead=120,
        cause_of_death="Exorcised by developer",
        commits_count=1,
        sample_diff=""
    )

    epitaph = "Laid to rest with honor. Its lessons remain etched in git history forever."
    res = grant_final_rites(
        repo_path=repo_path,
        artifact=artifact,
        epitaph=epitaph,
        memorial_file="OFRENDA.md",
        delete_branch=delete_branch
    )

    console.print(f"[green]🕯️ Tombstone erected in:[/green] [bold yellow]{res['memorial_path']}[/bold yellow]")
    if res["branch_deleted"]:
        console.print(f"[red]🧹 Branch {target} has been safely purged from git memory.[/red]")
    else:
        console.print(f"[dim]Note: Branch was preserved in git. Pass --delete to purge it.[/dim]")
    return 0


def handle_web(host: str, port: int) -> int:
    """Launch the FastAPI gothic web dashboard."""
    import uvicorn
    console.print(BANNER)
    console.print(f"[bold magenta]🔮 Awakening The Git Catacombs on[/bold magenta] [bold cyan]http://{host}:{port}[/bold cyan]...\n")
    uvicorn.run("app.web.server:app", host=host, port=port, reload=False)
    return 0


def main() -> int:
    """Entry point for CLI execution."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        return handle_scan(args.repo, args.demo)
    elif args.command == "seance":
        return handle_seance(args.repo, args.target, args.demo)
    elif args.command == "resurrect":
        return handle_resurrect(args.repo, args.target, args.output)
    elif args.command == "exorcise":
        return handle_exorcise(args.repo, args.target, args.delete)
    elif args.command == "web":
        return handle_web(args.host, args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
