import httpx
import os

DEFAULT_HOST = "http://localhost:11434"


def query_ollama(activity: str, model: str = "llama3.2", fmt: str = "markdown", target_date: str = "") -> str:
    host = os.environ.get("OLLAMA_HOST", DEFAULT_HOST)

    prompt = (
        f"You are a daily standup report generator. Given the following git activity "
        f"for {target_date}, produce a structured standup report.\n\n"
        f"Format the report with these sections:\n"
        f"- What I did yesterday\n"
        f"- What I'll do today\n"
        f"- Blockers\n\n"
        f"Git Activity:\n{activity}\n\n"
        f"Standup Report ({fmt} format):"
    )

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3},
    }

    try:
        resp = httpx.post(f"{host}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()
    except httpx.ConnectError:
        return "Error: Cannot connect to Ollama. Is it running?"
    except httpx.TimeoutException:
        return "Error: Ollama request timed out. Try a smaller model."
    except Exception as e:
        return f"Error: {str(e)}"
