import os
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
MODEL = os.getenv("LLM_MODEL", "claude-sonnet-4-6")


def ask(system: str, user: str, max_tokens: int = 1000) -> str:
    r = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return r.content[0].text.strip()
