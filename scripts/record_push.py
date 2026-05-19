from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HISTORY_FILE = ROOT / "PROJECT_VERSION_HISTORY.md"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def append_push_record() -> None:
    branch = git("branch", "--show-current") or "detached"
    commit = git("rev-parse", "--short", "HEAD")
    remote = git("remote", "get-url", "origin")
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    timezone = f"{timestamp[:-2]}:{timestamp[-2:]}"
    line = f"| {timezone} | push | `{branch}` | `{commit}` | `{remote}` |\n"

    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text(
            "# 项目版本回退记录\n\n| 时间 | 类型 | 当前分支 | 提交 | 远程 |\n| --- | --- | --- | --- | --- |\n",
            encoding="utf-8",
        )

    content = HISTORY_FILE.read_text(encoding="utf-8")
    HISTORY_FILE.write_text(content.rstrip() + "\n" + line, encoding="utf-8")


if __name__ == "__main__":
    append_push_record()
