"""Summarise a package's PyPI description with the course's chat model service."""

from databricks_openai import DatabricksOpenAI

PROMPT = "Summarise this PyPI package description in exactly three lines:\n\n{description}"


def summarise(
    description: str, llm_endpoint: str, client: DatabricksOpenAI | None = None
) -> tuple[str, dict[str, int]]:
    """Return the three-line summary and the token usage of the call."""
    client = client or DatabricksOpenAI(use_ai_gateway=True)
    response = client.chat.completions.create(
        model=llm_endpoint,
        messages=[{"role": "user", "content": PROMPT.format(description=description[:6000])}],
        max_tokens=1000,
    )
    usage = response.usage
    tokens = {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
    }
    return response.choices[0].message.content, tokens
