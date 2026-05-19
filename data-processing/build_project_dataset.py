from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from prepare_kaggle_data import DATA_DIR, sha256


KAGGLE_CSV = DATA_DIR / "kaggle_jobs_combined.csv"
MOHRSS_CSV = DATA_DIR / "mohrss_public_jobs.csv"
PROJECT_CSV = DATA_DIR / "project_jobs_real.csv"
PROJECT_METADATA = DATA_DIR / "project_jobs_real_metadata.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="合并 Kaggle 与公共招聘网真实岗位数据")
    parser.add_argument("--output", type=Path, default=PROJECT_CSV)
    args = parser.parse_args()

    frames = []
    for path in [KAGGLE_CSV, MOHRSS_CSV]:
        if not path.exists():
            raise FileNotFoundError(path)
        frames.append(pd.read_csv(path, dtype=str).fillna(""))

    df = pd.concat(frames, ignore_index=True)
    df["dedupe_key"] = df["source_ref"].astype(str) + ":" + df["job_id"].astype(str)
    df.loc[df["job_id"].eq(""), "dedupe_key"] = (
        df["source_ref"].astype(str)
        + ":"
        + df["job_title"].astype(str)
        + ":"
        + df["company_name"].astype(str)
        + ":"
        + df["city"].astype(str)
    )
    df = df.drop_duplicates("dedupe_key").drop(columns=["dedupe_key"])
    df = df[df["job_title"].astype(str).str.strip().ne("")]
    df = df[df["city"].astype(str).str.strip().ne("")]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False, encoding="utf-8-sig")

    province_counts = df["province"].replace("", "未知").value_counts().to_dict()
    source_counts = df["source_dataset"].value_counts().to_dict()
    salary_rows = int(df["salary"].astype(str).str.strip().ne("").sum())
    metadata = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "output": str(args.output.relative_to(DATA_DIR.parent.parent)),
        "sha256": sha256(args.output),
        "rows": int(len(df)),
        "salary_non_empty_rows": salary_rows,
        "province_count": int(df["province"].replace("", pd.NA).dropna().nunique()),
        "province_counts": {str(key): int(value) for key, value in province_counts.items()},
        "source_counts": {str(key): int(value) for key, value in source_counts.items()},
        "coverage_note": "Mainland province-level coverage is completed by China Public Recruitment Network. Kaggle data is retained as a real job sample source and salary-rich source.",
    }
    PROJECT_METADATA.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
