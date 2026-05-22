import json
import logging
from typing import Any

from app.core.config import get_settings


logger = logging.getLogger(__name__)


def ai_available() -> bool:
    return get_ai_config() is not None


def request_ai_json(system_prompt: str, payload: dict[str, Any]) -> Any | None:
    config = get_ai_config()
    if config is None:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        logger.warning("OpenAI SDK is not installed; falling back to local rules.")
        return None

    try:
        client = OpenAI(
            base_url=config["base_url"],
            api_key=config["api_key"],
            timeout=config["timeout"],
            default_headers=config["headers"],
        )
        completion = client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
            temperature=0.2,
        )
        content = completion.choices[0].message.content or ""
        return parse_json_content(content)
    except Exception as exc:  # noqa: BLE001 - AI calls must not break core APIs.
        logger.warning("AI request failed; falling back to local rules: %s", exc)
        return None


def get_ai_config() -> dict[str, Any] | None:
    settings = get_settings()
    if not settings.ai_enabled:
        return None

    provider = resolve_provider_config()
    if provider is None:
        return None
    api_key, base_url, model = provider
    headers = build_default_headers(base_url)

    return {
        "api_key": api_key,
        "base_url": base_url.rstrip("/"),
        "model": model,
        "timeout": settings.ai_timeout_seconds,
        "headers": headers,
    }


def resolve_provider_config() -> tuple[str, str, str] | None:
    settings = get_settings()

    if settings.ai_api_key.strip():
        return (
            settings.ai_api_key.strip(),
            settings.ai_base_url.strip(),
            settings.ai_model.strip(),
        )

    if settings.openrouter_api_key.strip():
        return (
            settings.openrouter_api_key.strip(),
            settings.openrouter_base_url.strip(),
            settings.openrouter_model.strip(),
        )

    if settings.zenmux_api_key.strip():
        return (
            settings.zenmux_api_key.strip(),
            settings.zenmux_base_url.strip(),
            settings.zenmux_model.strip(),
        )

    return None


def build_default_headers(base_url: str) -> dict[str, str]:
    settings = get_settings()
    headers: dict[str, str] = {}
    if "openrouter.ai" not in base_url:
        return headers

    if settings.openrouter_app_name.strip():
        headers["X-Title"] = settings.openrouter_app_name.strip()
    if settings.openrouter_site_url.strip():
        headers["HTTP-Referer"] = settings.openrouter_site_url.strip()
    return headers


def parse_json_content(content: str) -> Any:
    text = content.strip()
    if text.startswith("```"):
        lines = [line for line in text.splitlines() if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start_positions = [pos for pos in (text.find("{"), text.find("[")) if pos >= 0]
    if not start_positions:
        raise ValueError("AI response does not contain JSON.")

    start = min(start_positions)
    end = max(text.rfind("}"), text.rfind("]"))
    if end <= start:
        raise ValueError("AI response JSON is incomplete.")
    return json.loads(text[start : end + 1])
