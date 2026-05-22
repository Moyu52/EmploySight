from __future__ import annotations

import secrets
import threading
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Header, HTTPException, Query, Request, status

from app.core.config import get_settings
from app.core.passwords import verify_pbkdf2_password
from app.schemas import (
    AdminBannedIpRecord,
    AdminDeleteAuditRequest,
    AdminDeleteAuditResponse,
    AdminDeleteSecurityError,
    AdminLoginRequest,
    AdminLoginResponse,
    AdminUnbanIpRequest,
    AdminUnbanIpResponse,
    ApiResponse,
    PlatformLoginEventRequest,
)
from app.services.audit_log import append_login_event, delete_login_event, extract_ip_snapshot, list_login_events


router = APIRouter()
_SESSIONS: dict[str, dict[str, str]] = {}
_DELETE_FAILURES: dict[str, dict[str, int | str]] = {}
_DELETE_SECURITY_LOCK = threading.Lock()
_SESSION_TTL = timedelta(hours=8)


def _expires_at() -> datetime:
    return datetime.now(timezone.utc) + _SESSION_TTL


def _make_session(username: str) -> tuple[str, str]:
    token = secrets.token_urlsafe(32)
    expires_at = _expires_at().isoformat(timespec="seconds")
    _SESSIONS[token] = {"username": username, "expiresAt": expires_at}
    return token, expires_at


def _constant_time_equal(left: str, right: str) -> bool:
    return secrets.compare_digest(left.encode("utf-8"), right.encode("utf-8"))


def _verify_admin_secret(password: str, encoded_hash: str, purpose: str) -> bool:
    settings = get_settings()
    if not settings.admin_security_pepper or not encoded_hash:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin security hash is not configured",
        )
    return verify_pbkdf2_password(
        password=password,
        encoded_hash=encoded_hash,
        pepper=settings.admin_security_pepper,
        purpose=purpose,
    )


def _delete_security_key(request: Request) -> str:
    ip_snapshot = extract_ip_snapshot(request)
    return ip_snapshot["observedIp"] or ip_snapshot["reportedIp"] or "unknown"


def _delete_blocked_until(entry: dict[str, int | str]) -> datetime | None:
    value = str(entry.get("blockedUntil") or "")
    if not value:
        return None
    try:
        blocked_until = datetime.fromisoformat(value)
    except ValueError:
        return None
    if blocked_until.tzinfo is None:
        return blocked_until.replace(tzinfo=timezone.utc)
    return blocked_until


def _delete_security_payload(
    *,
    attempts: int,
    max_attempts: int,
    banned: bool = False,
    blocked_until: datetime | None = None,
) -> dict[str, int | bool | str]:
    return AdminDeleteSecurityError(
        remainingAttempts=max(max_attempts - attempts, 0),
        maxAttempts=max_attempts,
        banned=banned,
        blockedUntil=blocked_until.isoformat(timespec="seconds") if blocked_until else "",
    ).model_dump()


def _raise_delete_security_error(
    *,
    detail: str,
    attempts: int,
    max_attempts: int,
    banned: bool = False,
    blocked_until: datetime | None = None,
) -> None:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "message": detail,
            **_delete_security_payload(
                attempts=attempts,
                max_attempts=max_attempts,
                banned=banned,
                blocked_until=blocked_until,
            ),
        },
    )


def _require_delete_not_banned(request: Request) -> str:
    settings = get_settings()
    key = _delete_security_key(request)
    with _DELETE_SECURITY_LOCK:
        entry = _DELETE_FAILURES.get(key)
    if not entry:
        return key

    blocked_until = _delete_blocked_until(entry)
    now = datetime.now(timezone.utc)
    if blocked_until and blocked_until > now:
        _raise_delete_security_error(
            detail="当前 IP 删除操作已被临时封禁，请稍后再试。",
            attempts=int(entry.get("attempts") or settings.admin_delete_max_attempts),
            max_attempts=settings.admin_delete_max_attempts,
            banned=True,
            blocked_until=blocked_until,
        )

    if blocked_until and blocked_until <= now:
        with _DELETE_SECURITY_LOCK:
            _DELETE_FAILURES.pop(key, None)
    return key


def _register_delete_password_failure(key: str) -> None:
    settings = get_settings()
    max_attempts = max(settings.admin_delete_max_attempts, 1)
    with _DELETE_SECURITY_LOCK:
        attempts = int(_DELETE_FAILURES.get(key, {}).get("attempts") or 0) + 1
        blocked_until: datetime | None = None
        banned = attempts >= max_attempts
        if banned:
            ban_minutes = max(settings.admin_delete_ban_minutes, 1)
            blocked_until = datetime.now(timezone.utc) + timedelta(minutes=ban_minutes)

        _DELETE_FAILURES[key] = {
            "attempts": attempts,
            "blockedUntil": blocked_until.isoformat(timespec="seconds") if blocked_until else "",
        }

    if banned:
        _raise_delete_security_error(
            detail="删除密码错误次数过多，当前 IP 已被临时封禁。",
            attempts=attempts,
            max_attempts=max_attempts,
            banned=True,
            blocked_until=blocked_until,
        )

    _raise_delete_security_error(
        detail=f"删除密码错误，还剩 {max_attempts - attempts} 次机会，否则当前 IP 将被封禁。",
        attempts=attempts,
        max_attempts=max_attempts,
    )


def _active_delete_bans() -> list[dict[str, int | str]]:
    now = datetime.now(timezone.utc)
    records: list[dict[str, int | str]] = []
    expired: list[str] = []
    with _DELETE_SECURITY_LOCK:
        for ip, entry in _DELETE_FAILURES.items():
            blocked_until = _delete_blocked_until(entry)
            if not blocked_until:
                continue
            if blocked_until <= now:
                expired.append(ip)
                continue
            records.append(
                AdminBannedIpRecord(
                    ip=ip,
                    attempts=int(entry.get("attempts") or 0),
                    blockedUntil=blocked_until.isoformat(timespec="seconds"),
                ).model_dump()
            )
        for ip in expired:
            _DELETE_FAILURES.pop(ip, None)
    return records


def _require_admin(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing admin token")
    token = authorization.split(" ", 1)[1].strip()
    session = _SESSIONS.get(token)
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")

    expires_at = datetime.fromisoformat(session["expiresAt"])
    if expires_at <= datetime.now(timezone.utc):
        _SESSIONS.pop(token, None)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin token expired")
    return session["username"]


@router.post("/login", response_model=ApiResponse)
def admin_login(payload: AdminLoginRequest, request: Request) -> ApiResponse:
    settings = get_settings()
    valid_username = _constant_time_equal(payload.username, settings.admin_username)
    valid_password = _constant_time_equal(payload.password, settings.admin_password)

    if not (valid_username and valid_password):
        append_login_event(
            request=request,
            username=payload.username,
            source="admin",
            status="failed",
            note="管理员登录失败",
        )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")

    token, expires_at = _make_session(payload.username)
    append_login_event(
        request=request,
        username=payload.username,
        source="admin",
        status="success",
        note="管理员登录成功",
    )
    return ApiResponse(data=AdminLoginResponse(token=token, username=payload.username, expiresAt=expires_at))


@router.post("/login-events", response_model=ApiResponse)
def record_platform_login(payload: PlatformLoginEventRequest, request: Request) -> ApiResponse:
    record = append_login_event(
        request=request,
        username=payload.username,
        source="platform",
        status="success",
        note="统一平台登录",
    )
    return ApiResponse(data=record)


@router.get("/login-events", response_model=ApiResponse)
def query_login_events(
    authorization: str = Header(default="", alias="Authorization"),
    q: str = Query(default="", max_length=120),
    limit: int = Query(default=100, ge=1, le=500),
) -> ApiResponse:
    _require_admin(authorization)
    return ApiResponse(data=list_login_events(query=q, limit=limit))


@router.get("/banned-ips", response_model=ApiResponse)
def query_banned_ips(
    authorization: str = Header(default="", alias="Authorization"),
) -> ApiResponse:
    _require_admin(authorization)
    return ApiResponse(data=_active_delete_bans())


@router.post("/unban-ip", response_model=ApiResponse)
def unban_ip(
    payload: AdminUnbanIpRequest,
    authorization: str = Header(default="", alias="Authorization"),
) -> ApiResponse:
    _require_admin(authorization)
    settings = get_settings()
    if not _verify_admin_secret(
        payload.unbanPassword,
        settings.admin_unban_password_hash,
        "admin-unban",
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid unban password")

    with _DELETE_SECURITY_LOCK:
        removed = _DELETE_FAILURES.pop(payload.ip.strip(), None) is not None
    return ApiResponse(data=AdminUnbanIpResponse(ip=payload.ip.strip(), unbanned=removed))


@router.delete("/login-events/{record_id}", response_model=ApiResponse)
def delete_login_event_record(
    record_id: str,
    payload: AdminDeleteAuditRequest,
    request: Request,
    authorization: str | None = Header(default=None),
) -> ApiResponse:
    _require_admin(authorization)
    delete_security_key = _require_delete_not_banned(request)
    settings = get_settings()
    if not _verify_admin_secret(
        payload.deletePassword,
        settings.admin_delete_password_hash,
        "admin-delete",
    ):
        _register_delete_password_failure(delete_security_key)
    try:
        _, backup_file = delete_login_event(record_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit record not found") from exc
    with _DELETE_SECURITY_LOCK:
        _DELETE_FAILURES.pop(delete_security_key, None)
    return ApiResponse(
        data=AdminDeleteAuditResponse(deletedId=record_id, backupFile=backup_file.name)
    )
