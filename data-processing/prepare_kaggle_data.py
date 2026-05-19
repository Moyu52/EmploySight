from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "raw"
DATA_DIR = ROOT / "data"

POLARTECH_ZIP = RAW_DIR / "kaggle_china_jobs_data.zip"
TECHSALERATOR_ZIP = RAW_DIR / "kaggle_job_posting_data_in_china.zip"
COMBINED_CSV = DATA_DIR / "kaggle_jobs_combined.csv"
METADATA_JSON = DATA_DIR / "kaggle_jobs_metadata.json"

CITY_PROVINCE = {
    "Beijing": ("北京", "北京"),
    "Shanghai": ("上海", "上海"),
    "Guangzhou": ("广东", "广州"),
    "Shenzhen": ("广东", "深圳"),
    "Wuhan": ("湖北", "武汉"),
    "Jiaxing": ("浙江", "嘉兴"),
    "Qingdao": ("山东", "青岛"),
    "Hangzhou": ("浙江", "杭州"),
    "Chengdu": ("四川", "成都"),
    "Changzhou": ("江苏", "常州"),
    "Shenyang": ("辽宁", "沈阳"),
    "Jinan": ("山东", "济南"),
    "Suzhou": ("江苏", "苏州"),
    "Hong Kong": ("香港", "香港"),
    "Chongqing": ("重庆", "重庆"),
    "Changchun": ("吉林", "长春"),
    "Changsha": ("湖南", "长沙"),
    "Weihai": ("山东", "威海"),
    "Taishan": ("广东", "台山"),
    "Rizhao": ("山东", "日照"),
    "Wuxi": ("江苏", "无锡"),
    "Tianjin": ("天津", "天津"),
}

CITY_COORDS = {
    "北京": (116.407526, 39.904030),
    "上海": (121.473701, 31.230416),
    "广州": (113.264385, 23.129112),
    "深圳": (114.057868, 22.543099),
    "武汉": (114.305393, 30.593099),
    "嘉兴": (120.755486, 30.746129),
    "青岛": (120.382639, 36.067082),
    "杭州": (120.155070, 30.274085),
    "成都": (104.066541, 30.572269),
    "常州": (119.974092, 31.811313),
    "沈阳": (123.431475, 41.805698),
    "济南": (117.120128, 36.652069),
    "苏州": (120.585315, 31.298886),
    "香港": (114.169361, 22.319303),
    "重庆": (106.551643, 29.562849),
    "长春": (125.323544, 43.817072),
    "长沙": (112.938814, 28.228209),
    "威海": (122.120420, 37.513068),
    "台山": (112.793812, 22.251947),
    "日照": (119.526888, 35.416377),
    "无锡": (120.311910, 31.491170),
    "天津": (117.200983, 39.084158),
    "南京": (118.796877, 32.060255),
    "哈尔滨": (126.534967, 45.803775),
    "石家庄": (114.514976, 38.042007),
    "太原": (112.548879, 37.870590),
    "宁波": (121.550357, 29.874556),
    "合肥": (117.227239, 31.820586),
    "西安": (108.939770, 34.341575),
    "郑州": (113.625368, 34.746599),
    "大连": (121.614682, 38.914003),
    "贵阳": (106.630153, 26.647661),
    "呼和浩特": (111.749181, 40.842585),
    "福州": (119.296494, 26.074508),
}

PROVINCE_SUFFIX_RE = re.compile(r"(省|市|自治区|壮族自治区|回族自治区|维吾尔自治区|特别行政区)$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def first_csv_name(zip_path: Path) -> str:
    with zipfile.ZipFile(zip_path) as archive:
        for name in archive.namelist():
            if name.lower().endswith(".csv"):
                return name
    raise FileNotFoundError(f"{zip_path} does not contain a CSV file")


def clean_province(value: str) -> str:
    value = (value or "").strip()
    value = PROVINCE_SUFFIX_RE.sub("", value)
    return value.replace("北京省", "北京").replace("上海省", "上海")


def clean_city(value: str) -> str:
    value = (value or "").strip()
    value = value.split("·", 1)[0]
    value = value.replace("市", "")
    return value


def parse_area_detail(source: str) -> tuple[str, str]:
    if not source:
        return "", ""
    try:
        detail = ast.literal_eval(source)
    except (SyntaxError, ValueError):
        return "", ""
    province = clean_province(detail.get("provinceString", ""))
    city = clean_city(detail.get("cityString", ""))
    if province == "深圳":
        province = "广东"
        city = city or "深圳"
    return province, city


def normalize_polartech() -> tuple[list[dict[str, str]], dict[str, int | str]]:
    rows: list[dict[str, str]] = []
    csv_name = first_csv_name(POLARTECH_ZIP)
    with zipfile.ZipFile(POLARTECH_ZIP) as archive:
        with archive.open(csv_name) as raw:
            reader = csv.DictReader((line.decode("utf-8-sig", errors="replace") for line in raw))
            for row in reader:
                province, city = parse_area_detail(row.get("jobAreaLevelDetail", ""))
                if not city:
                    city = clean_city(row.get("jobAreaString", ""))
                if not province:
                    province = clean_province(row.get("province_name", ""))
                if not province and city in {"北京", "上海", "天津", "重庆"}:
                    province = city
                if not province and city == "深圳":
                    province = "广东"

                longitude = row.get("lon", "").strip()
                latitude = row.get("lat", "").strip()
                if (not longitude or not latitude) and city in CITY_COORDS:
                    longitude, latitude = map(str, CITY_COORDS[city])

                rows.append(
                    {
                        "source_dataset": "Kaggle China Jobs Data",
                        "source_ref": "polartech/china-jobs-data",
                        "job_id": row.get("jobId", "").strip(),
                        "job_title": row.get("jobName", "").strip(),
                        "company_name": row.get("fullCompanyName", "").strip() or row.get("companyName", "").strip(),
                        "city": city,
                        "province": province,
                        "salary": row.get("provideSalaryString", "").strip(),
                        "education": row.get("degreeString", "").strip() or "不限",
                        "experience": row.get("workYearString", "").strip() or "不限",
                        "industry": row.get("industryType1Str", "").strip() or row.get("industry_1_name", "").strip(),
                        "major": row.get("major1Str", "").strip() or row.get("major2Str", "").strip(),
                        "company_size": row.get("companySizeString", "").strip(),
                        "company_type": row.get("companyTypeString", "").strip(),
                        "publish_date": row.get("issueDateString", "").strip(),
                        "description": " ".join(
                            part
                            for part in [
                                row.get("jobName", "").strip(),
                                row.get("industryType1Str", "").strip(),
                                row.get("industryType2Str", "").strip(),
                                row.get("function_1_name", "").strip(),
                                row.get("function_2_name", "").strip(),
                                row.get("major1Str", "").strip(),
                            ]
                            if part
                        ),
                        "longitude": longitude,
                        "latitude": latitude,
                        "source_url": "https://www.kaggle.com/datasets/polartech/china-jobs-data",
                    }
                )
    return rows, {"csv_file": csv_name, "raw_rows": len(rows)}


def parse_location_data(source: str) -> tuple[str, str, bool]:
    if not source:
        return "", "", False
    try:
        locations = json.loads(source)
    except json.JSONDecodeError:
        return "", "", False
    if not isinstance(locations, list):
        return "", "", False
    for location in locations:
        if not isinstance(location, dict):
            continue
        if location.get("country") != "China":
            continue
        city_en = location.get("city") or ""
        province, city = CITY_PROVINCE.get(city_en, ("", ""))
        return province, city, True
    return "", "", False


def normalize_techsalerator() -> tuple[list[dict[str, str]], dict[str, int | str]]:
    rows: list[dict[str, str]] = []
    csv_name = first_csv_name(TECHSALERATOR_ZIP)
    with zipfile.ZipFile(TECHSALERATOR_ZIP) as archive:
        with archive.open(csv_name) as raw:
            reader = csv.DictReader((line.decode("utf-8-sig", errors="replace") for line in raw))
            total = 0
            for row in reader:
                total += 1
                province, city, is_china = parse_location_data(row.get("Location Data", ""))
                if not is_china and "China" not in (row.get("Location", "")):
                    continue
                if not city:
                    parts = [part.strip() for part in row.get("Location", "").split(",")]
                    province, city = CITY_PROVINCE.get(parts[0], ("", parts[0] if parts and parts[0] != "China" else ""))
                if not city:
                    continue

                longitude = latitude = ""
                if city in CITY_COORDS:
                    longitude, latitude = map(str, CITY_COORDS[city])

                title = row.get("Job Opening Title", "").strip()
                category = row.get("Category", "").strip().replace("_", " ")
                keywords = row.get("Keywords", "").strip()
                description = row.get("Description", "").strip()
                rows.append(
                    {
                        "source_dataset": "Kaggle Job Posting Data in China",
                        "source_ref": "techsalerator/job-posting-data-in-china",
                        "job_id": hashlib.sha1(row.get("Job Opening URL", "").encode("utf-8")).hexdigest()[:16],
                        "job_title": title,
                        "company_name": row.get("Website Domain", "").strip(),
                        "city": city,
                        "province": province,
                        "salary": row.get("Salary", "").strip(),
                        "education": "不限",
                        "experience": "不限" if row.get("Seniority", "") == "non_manager" else row.get("Seniority", "").strip(),
                        "industry": category,
                        "major": "",
                        "company_size": "",
                        "company_type": "",
                        "publish_date": row.get("First Seen At", "").strip(),
                        "description": " ".join(part for part in [title, category, keywords, description] if part),
                        "longitude": longitude,
                        "latitude": latitude,
                        "source_url": row.get("Job Opening URL", "").strip()
                        or "https://www.kaggle.com/datasets/techsalerator/job-posting-data-in-china",
                    }
                )
    return rows, {"csv_file": csv_name, "raw_rows": total, "china_rows": len(rows)}


def write_csv(rows: list[dict[str, str]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source_dataset",
        "source_ref",
        "job_id",
        "job_title",
        "company_name",
        "city",
        "province",
        "salary",
        "education",
        "experience",
        "industry",
        "major",
        "company_size",
        "company_type",
        "publish_date",
        "description",
        "longitude",
        "latitude",
        "source_url",
    ]
    with COMBINED_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if not POLARTECH_ZIP.exists() or not TECHSALERATOR_ZIP.exists():
        raise FileNotFoundError("Missing Kaggle zip files in data-processing/raw")

    polartech_rows, polartech_meta = normalize_polartech()
    techsalerator_rows, techsalerator_meta = normalize_techsalerator()
    rows = polartech_rows + techsalerator_rows
    write_csv(rows)

    metadata = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "combined_csv": str(COMBINED_CSV.relative_to(ROOT.parent)),
        "combined_sha256": sha256(COMBINED_CSV),
        "combined_rows": len(rows),
        "salary_non_empty_rows": sum(1 for row in rows if row["salary"]),
        "sources": [
            {
                "name": "Kaggle China Jobs Data",
                "ref": "polartech/china-jobs-data",
                "url": "https://www.kaggle.com/datasets/polartech/china-jobs-data",
                "local_zip": str(POLARTECH_ZIP.relative_to(ROOT.parent)),
                "zip_sha256": sha256(POLARTECH_ZIP),
                **polartech_meta,
            },
            {
                "name": "Kaggle Job Posting Data in China",
                "ref": "techsalerator/job-posting-data-in-china",
                "url": "https://www.kaggle.com/datasets/techsalerator/job-posting-data-in-china",
                "local_zip": str(TECHSALERATOR_ZIP.relative_to(ROOT.parent)),
                "zip_sha256": sha256(TECHSALERATOR_ZIP),
                **techsalerator_meta,
                "note": "The original CSV contains global postings; only records with country=China are retained.",
            },
        ],
    }
    METADATA_JSON.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
