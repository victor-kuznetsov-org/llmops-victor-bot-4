from unittest.mock import MagicMock

from pkgscout.summarise import summarise


def test_summarise_returns_text_and_usage() -> None:
    client = MagicMock()
    resp = client.chat.completions.create.return_value
    resp.choices[0].message.content = "a\nb\nc"
    resp.usage.prompt_tokens, resp.usage.completion_tokens, resp.usage.total_tokens = 5, 3, 8
    text, usage = summarise("desc", "course_ops.gateway.chat", client=client)
    assert text == "a\nb\nc"
    assert usage == {"prompt_tokens": 5, "completion_tokens": 3, "total_tokens": 8}
    assert client.chat.completions.create.call_args.kwargs["model"] == "course_ops.gateway.chat"
