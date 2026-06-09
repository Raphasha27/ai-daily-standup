# AI Daily Standup

A CLI tool that generates daily standup reports from your git activity using local AI (Ollama).

## Features

- Scans git commits across repos for the day and generates structured standup reports
- Groups work by project, type (feature, fix, chore), and status
- Generates "What I did yesterday", "What I'll do today", "Blockers" format
- Supports multiple repos in a workspace
- Optional Slack/Markdown output formats
- Runs 100% locally via Ollama

## Installation

```bash
pip install ai-daily-standup
```

Or clone and install:

```bash
git clone https://github.com/Raphasha27/ai-daily-standup.git
cd ai-daily-standup
pip install -e .
```

## Usage

```bash
# Generate standup from today's git activity
aids generate

# For a specific date
aids generate --date 2026-06-01

# Include multiple repos
aids generate --repo /path/to/repo1 --repo /path/to/repo2

# Output format
aids generate --format markdown
aids generate --format slack

# Include branch activity
aids generate --with-branches
```

## Example Output

```markdown
# Daily Standup — 2026-06-02

## What I did yesterday
- **ai-commit-writer**: Implemented interactive mode for commit message review
- **ai-meeting-minutes**: Added JSON output format support
- **infrastructure**: Updated CI pipeline for Python 3.12

## What I'll do today
- Add unit tests for ai-pr-description
- Review PR #42 in ai-commit-writer

## Blockers
- None
```

## Configuration

Create `~/.config/aids/config.toml`:

```toml
[defaults]
repos = ["/path/to/repo1", "/path/to/repo2"]
model = "llama3.2"
format = "markdown"
```

<br/>

---

<h3 align="center">🐍 Part of the <a href="https://github.com/Raphasha27">Raphasha27</a> Ecosystem</h3>

<p align="center">
  <a href="https://github.com/Raphasha27/Raphasha27">
    <img src="https://img.shields.io/badge/Back_to_Profile-0D1117?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  &nbsp;
  <a href="https://raphasha27.github.io/Raphasha27/ai-snake-game/">
    <img src="https://img.shields.io/badge/▶_Play_AI_Snake-0EA5E9?style=for-the-badge&logo=javascript&logoColor=white" />
  </a>
</p>

## License

MIT
