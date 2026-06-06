"""Provider-agnostic LLM router"""

from __future__ import annotations

_OPENROUTER_BASE = "https://openrouter.ai/api/v1"

# Providers with OpenAI-compatible APIs — same code path, different base_url
_COMPAT_BASES: dict[str, str] = {
    "openrouter": "https://openrouter.ai/api/v1",
    "deepseek":   "https://api.deepseek.com/v1",
    "kimi":       "https://api.moonshot.cn/v1",
    "nemotron":   "https://integrate.api.nvidia.com/v1",
}


def _openai_compat(base_url: str, api_key: str, model: str, prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=base_url)
    return (
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
        )
        .choices[0]
        .message.content
    )


def call_llm(provider: str, model: str, api_key: str, prompt: str) -> str:
    if provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    if provider in _COMPAT_BASES:
        return _openai_compat(_COMPAT_BASES[provider], api_key, model, prompt)

    if provider == "openai":
        return _openai_compat("https://api.openai.com/v1", api_key, model, prompt)

    if provider == "ollama":
        import ollama as _ollama
        return _ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )["message"]["content"]

    raise ValueError(f"Unsupported provider: {provider!r}")
