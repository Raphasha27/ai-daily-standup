"""ai-daily-standup - Generate standup reports from git activity."""

import subprocess, os, sys
from datetime import datetime, timedelta
try:
    import httpx, typer
    from rich.console import Console
    from rich.markdown import Markdown
except ImportError:
    print("Missing: pip install httpx typer rich"); sys.exit(1)

app = typer.Typer()
console = Console()
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

PROMPT = """Summarize the following git activity into a daily standup report.

Use this format:
## What I did yesterday
## What I'll do today
## Blockers

GIT ACTIVITY:
{activity}"""


def get_git_activity(since_hours=24) -> str:
    since = (datetime.now() - timedelta(hours=since_hours)).strftime("%Y-%m-%dT%H:%M:%S")
    log = subprocess.run(["git", "log", "--oneline", "--since=" + since], capture_output=True, text=True).stdout
    diff = subprocess.run(["git", "diff", "@{1.day.ago}"], capture_output=True, text=True, shell=True).stdout
    branches = subprocess.run(["git", "branch", "--list"], capture_output=True, text=True).stdout
    return f"Commits:\n{log}\n\nBranches:\n{branches}\n\nRecent changes:\n{diff[:3000]}"


def query_ollama(prompt: str) -> str:
    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(f"{OLLAMA_HOST}/api/generate", json={
                "model": OLLAMA_MODEL, "prompt": prompt,
                "stream": False, "options": {"temperature": 0.3}
            })
            resp.raise_for_status()
            return resp.json().get("response", "")
    except httpx.HTTPError as e:
        console.print(f"[red]Error: {e}[/]"); sys.exit(1)


@app.command()
def generate(
    hours: int = typer.Option(24, "--hours", "-h", help="Hours of activity to include"),
    model: str = typer.Option(OLLAMA_MODEL, "--model", "-m"),
) -> None:
    activity = get_git_activity(hours)
    console.print(f"[cyan]Generating standup for last {hours}h...[/]")
    result = query_ollama(PROMPT.format(activity=activity[:4000]))
    console.print(Markdown(result))

if __name__ == "__main__":
    app()
