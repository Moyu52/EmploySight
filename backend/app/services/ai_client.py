import json
import logging
from typing import Any

from app.core.config import get_settings


logger = logging.getLogger(__name__)


def ai_available() -> bool:
    settings = get_settings()
    return settings.ai_enabled and bool(settings.zenmux_api_key.strip())


def request_ai_json(system_prompt: str, payload: dict[str, Any]) -> Any | None:
    settings = get_settings()
    if not ai_available():
        return None

    try:
        from openai import OpenAI
    except ImportError:
        logger.warning("OpenAI SDK is not installed; falling back to local rules.")
        return None

    try:
        client = OpenAI(
            base_url=settings.zenmux_base_url,
            api_key=settings.zenmux_api_key,
            timeout=settings.ai_timeout_seconds,
        )
        completion = client.chat.completions.create(
            model=settings.zenmux_model,
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
