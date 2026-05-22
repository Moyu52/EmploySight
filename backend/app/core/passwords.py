from __future__ import annotations

import base64
import hashlib
import secrets


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))


def verify_pbkdf2_password(*, password: str, encoded_hash: str, pepper: str, purpose: str) -> bool:
    parts = encoded_hash.split("$")
    if len(parts) != 5 or parts[0] != "pbkdf2_sha256" or parts[1] != "v1":
        return False

    try:
        iterations = int(parts[2])
        salt = _b64decode(parts[3])
        expected = _b64decode(parts[4])
    except (ValueError, TypeError):
        return False

    material = f"{purpose}:{pepper}:{password}".encode("utf-8")
    actual = hashlib.pbkdf2_hmac("sha256", material, salt, iterations)
    return secrets.compare_digest(actual, expected)
