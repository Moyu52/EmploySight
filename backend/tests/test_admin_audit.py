from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app
from app.routers import admin as admin_router


TEST_PEPPER = "test-pepper"
TEST_DELETE_HASH = "pbkdf2_sha256$v1$120000$N_s7PMERQ28oOmhDRxW1QA$DBlNG3eegpspcIg-IYivYshFkQbfoBuOAYbgnX4_Ei4"
TEST_UNBAN_HASH = "pbkdf2_sha256$v1$120000$q2aVBi_ibn1Ja4rZIEAWHw$Hdy7LjC4YuMqh2foT_CKduCevXqIQ1Bi4Mr6g70s0Fk"


def configure_admin_env(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "admin123")
    monkeypatch.setenv("ADMIN_SECURITY_PEPPER", TEST_PEPPER)
    monkeypatch.setenv("ADMIN_DELETE_PASSWORD_HASH", TEST_DELETE_HASH)
    monkeypatch.setenv("ADMIN_UNBAN_PASSWORD_HASH", TEST_UNBAN_HASH)
    monkeypatch.setenv("ADMIN_DELETE_MAX_ATTEMPTS", "3")
    monkeypatch.setenv("ADMIN_DELETE_BAN_MINUTES", "30")
    monkeypatch.setenv("AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.setenv("AUDIT_BACKUP_DIR", str(tmp_path / "backups"))
    get_settings.cache_clear()


def test_admin_audit_login_query_and_delete(tmp_path, monkeypatch) -> None:
    admin_router._DELETE_FAILURES.clear()
    configure_admin_env(tmp_path, monkeypatch)

    client = TestClient(app)

    platform_response = client.post(
        "/api/admin/login-events",
        json={"username": "alice"},
        headers={"X-Forwarded-For": "198.51.100.9", "User-Agent": "pytest"},
    )
    assert platform_response.status_code == 200
    assert platform_response.json()["data"]["reportedIp"] == "198.51.100.9"

    login_response = client.post(
        "/api/admin/login",
        json={"username": "admin", "password": "admin123"},
        headers={"X-Real-IP": "203.0.113.10"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["data"]["token"]

    query_response = client.get(
        "/api/admin/login-events",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert query_response.status_code == 200
    records = query_response.json()["data"]
    assert any(record["username"] == "alice" for record in records)
    assert any(record["username"] == "admin" for record in records)

    record_id = records[0]["id"]
    delete_response = client.request(
        "DELETE",
        f"/api/admin/login-events/{record_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"deletePassword": "delete123"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["data"]["deletedId"] == record_id
    assert list((tmp_path / "backups").glob("*.jsonl"))

    admin_router._DELETE_FAILURES.clear()
    get_settings.cache_clear()


def test_admin_delete_password_failures_ban_request_ip(tmp_path, monkeypatch) -> None:
    admin_router._DELETE_FAILURES.clear()
    configure_admin_env(tmp_path, monkeypatch)

    client = TestClient(app)
    client.post("/api/admin/login-events", json={"username": "alice"})
    login_response = client.post("/api/admin/login", json={"username": "admin", "password": "admin123"})
    token = login_response.json()["data"]["token"]
    records = client.get("/api/admin/login-events", headers={"Authorization": f"Bearer {token}"}).json()["data"]
    record_id = records[0]["id"]

    first_failed = client.request(
        "DELETE",
        f"/api/admin/login-events/{record_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"deletePassword": "wrong"},
    )
    assert first_failed.status_code == 403
    first_detail = first_failed.json()["detail"]
    assert first_detail["remainingAttempts"] == 2
    assert first_detail["banned"] is False

    second_failed = client.request(
        "DELETE",
        f"/api/admin/login-events/{record_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"deletePassword": "wrong"},
    )
    assert second_failed.status_code == 403
    assert second_failed.json()["detail"]["remainingAttempts"] == 1

    third_failed = client.request(
        "DELETE",
        f"/api/admin/login-events/{record_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"deletePassword": "wrong"},
    )
    assert third_failed.status_code == 403
    third_detail = third_failed.json()["detail"]
    assert third_detail["remainingAttempts"] == 0
    assert third_detail["banned"] is True
    assert third_detail["blockedUntil"]

    blocked_delete = client.request(
        "DELETE",
        f"/api/admin/login-events/{record_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"deletePassword": "delete123"},
    )
    assert blocked_delete.status_code == 403
    assert blocked_delete.json()["detail"]["banned"] is True

    admin_router._DELETE_FAILURES.clear()
    get_settings.cache_clear()


def test_admin_can_list_and_unban_banned_ip(tmp_path, monkeypatch) -> None:
    admin_router._DELETE_FAILURES.clear()
    configure_admin_env(tmp_path, monkeypatch)

    client = TestClient(app)
    client.post("/api/admin/login-events", json={"username": "alice"})
    token = client.post(
        "/api/admin/login",
        json={"username": "admin", "password": "admin123"},
    ).json()["data"]["token"]
    record_id = client.get(
        "/api/admin/login-events",
        headers={"Authorization": f"Bearer {token}"},
    ).json()["data"][0]["id"]

    for _ in range(3):
        client.request(
            "DELETE",
            f"/api/admin/login-events/{record_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"deletePassword": "wrong"},
        )

    banned_response = client.get("/api/admin/banned-ips", headers={"Authorization": f"Bearer {token}"})
    assert banned_response.status_code == 200
    banned_ips = banned_response.json()["data"]
    assert len(banned_ips) == 1
    banned_ip = banned_ips[0]["ip"]

    wrong_unban = client.post(
        "/api/admin/unban-ip",
        headers={"Authorization": f"Bearer {token}"},
        json={"ip": banned_ip, "unbanPassword": "wrong"},
    )
    assert wrong_unban.status_code == 403

    unban_response = client.post(
        "/api/admin/unban-ip",
        headers={"Authorization": f"Bearer {token}"},
        json={"ip": banned_ip, "unbanPassword": "unban123"},
    )
    assert unban_response.status_code == 200
    assert unban_response.json()["data"]["unbanned"] is True

    delete_after_unban = client.request(
        "DELETE",
        f"/api/admin/login-events/{record_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"deletePassword": "delete123"},
    )
    assert delete_after_unban.status_code == 200

    admin_router._DELETE_FAILURES.clear()
    get_settings.cache_clear()
