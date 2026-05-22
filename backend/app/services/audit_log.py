from __future__ import annotations

import json
import shutil
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import Request

from app.core.config import get_settings


BACKEND_ROOT = Path(__file__).resolve().parents[2]
_LOCK = threading.Lock()


def _resolve_backend_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = BACKEND_ROOT / path
    return path


def _log_path() -> Path:
    return _resolve_backend_path(get_settings().audit_log_path)


def _backup_dir() -> Path:
    return _resolve_backend_path(get_settings().audit_backup_dir)


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _first_header_ip(value: str) -> str:
    if not value:
        return ""
    first_part = value.split(",", 1)[0].strip()
    if first_part.lower().startswith("for="):
        first_part = first_part[4:]
    return first_part.strip(" \"[]")


def extract_ip_snapshot(request: Request) -> dict[str, str]:
    forwarded = request.headers.get("forwarded", "")
    header_candidates = [
        request.headers.get("cf-connecting-ip", ""),
        request.headers.get("x-real-ip", ""),
        request.headers.get("x-forwarded-for", ""),
        forwarded.split(";", 1)[0] if forwarded else "",
    ]
    reported_ip = next((_first_header_ip(value) for value in header_candidates if _first_header_ip(value)), "")
    observed_ip = request.client.host if request.client else ""
    return {
        "reportedIp": reported_ip or observed_ip,
        "observedIp": observed_ip,
        "userAgent": request.headers.get("user-agent", ""),
    }


def append_login_event(
    *,
    request: Request,
    username: str,
    source: str,
    status: str = "success",
    note: str = "",
) -> dict[str, Any]:
    ip_snapshot = extract_ip_snapshot(request)
    record = {
        "id": uuid.uuid4().hex,
        "username": username,
        "loginTime": _now_iso(),
        "reportedIp": ip_snapshot["reportedIp"],
        "observedIp": ip_snapshot["observedIp"],
        "userAgent": ip_snapshot["userAgent"],
        "source": source,
        "status": status,
        "note": note,
    }

    path = _log_path()
    with _LOCK:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as audit_file:
            audit_file.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def list_login_events(query: str = "", limit: int = 100) -> list[dict[str, Any]]:
    path = _log_path()
    if not path.exists():
        return []

    query_text = query.strip().lower()
    records: list[dict[str, Any]] = []
    with _LOCK:
        lines = path.read_text(encoding="utf-8").splitlines()

    for line in reversed(lines):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if query_text and query_text not in json.dumps(record, ensure_ascii=False).lower():
            continue
        records.append(record)
        if len(records) >= limit:
            break
    return records


def delete_login_event(record_id: str) -> tuple[dict[str, Any], Path]:
    path = _log_path()
    if not path.exists():
        raise KeyError(record_id)

    with _LOCK:
        lines = path.read_text(encoding="utf-8").splitlines()
        records: list[dict[str, Any]] = []
        deleted: dict[str, Any] | None = None

        for line in lines:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("id") == record_id:
                deleted = record
                continue
            records.append(record)

        if deleted is None:
            raise KeyError(record_id)

        backup_dir = _backup_dir()
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = backup_dir / f"admin_login_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{record_id}.jsonl"
        shutil.copy2(path, backup_file)

        with path.open("w", encoding="utf-8") as audit_file:
            for record in records:
                audit_file.write(json.dumps(record, ensure_ascii=False) + "\n")

    return deleted, backup_file
