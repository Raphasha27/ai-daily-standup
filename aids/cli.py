import click
import subprocess
import os
from datetime import date
from .ollama import query_ollama


@click.group()
def main():
    pass


@main.command()
@click.option("--date", "-d", default=None, help="Date for standup (YYYY-MM-DD)")
@click.option("--repo", "-r", multiple=True, help="Path to git repo")
@click.option("--format", "-f", default="markdown", type=click.Choice(["markdown", "slack"]))
@click.option("--model", "-m", default="llama3.2")
@click.option("--with-branches", is_flag=True, help="Include branch activity")
def generate(date, repo, format, model, with_branches):
    target_date = date or str(date.today())

    if not repo:
        repo = find_git_repos()

    all_commits = []
    for r in repo:
        commits = get_daily_commits(r, target_date)
        if commits:
            all_commits.append(f"## {os.path.basename(r)}\n{commits}")

    if not all_commits:
        click.echo("No git activity found for " + target_date)
        return

    activity = "\n\n".join(all_commits)
    result = query_ollama(activity, model, format, target_date)

    if result.startswith("Error:"):
        click.echo(result, err=True)
        raise SystemExit(1)

    click.echo(result)


def find_git_repos() -> list:
    cwd = os.getcwd()
    repos = [cwd]
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, cwd=cwd
        )
        if result.returncode == 0:
            repos = [result.stdout.strip()]
    except Exception:
        pass
    return repos


def get_daily_commits(repo_path: str, target_date: str) -> str:
    try:
        result = subprocess.run(
            ["git", "log", f"--since={target_date}T00:00:00",
             f"--until={target_date}T23:59:59",
             "--oneline", "--format=%h %s (%an)"],
            capture_output=True, text=True, check=True, cwd=repo_path
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""
