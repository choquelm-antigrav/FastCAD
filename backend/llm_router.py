"""Provider-agnostic LLM router (T-202)"""

from __future__ import annotations


def call_llm(provider: str, model: str, api_key: str, prompt: str) -> str:
    """
    Route a prompt to the requested LLM provider and return the response text.

    Parameters
    ----------
    provider : one of 'anthropic', 'google', 'openai', 'ollama'
    model    : model name/ID as specified by the user
    api_key  : API key (ignored for ollama)
    prompt   : full prompt to send

    Raises
    ------
    ValueError  if provider is not supported
    """
    if provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    if provider == "google":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(model).generate_content(prompt).text

    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        return (
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            .choices[0]
            .message.content
        )

    if provider == "ollama":
        import ollama as _ollama
        return _ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )["message"]["content"]

    raise ValueError(f"Unsupported provider: {provider!r}")
