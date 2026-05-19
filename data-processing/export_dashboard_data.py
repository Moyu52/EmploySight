from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from pipeline import clean_jobs_for_coverage, extract_skills, parse_salary


ROOT = Path(__file__).resolve().parent.parent
DATA_INPUT = ROOT / "data-processing" / "data" / "project_jobs_real.csv"
OUTPUT_DIR = ROOT / "data-processing" / "output"
BACKEND_DATA = ROOT / "backend" / "app" / "services" / "demo_data.py"
FRONTEND_DATA = ROOT / "frontend" / "src" / "services" / "mockData.ts"
SNAPSHOT_META = ROOT / "data-processing" / "data" / "dashboard_snapshot_metadata.json"

ALL_REGIONS = [
    "北京",
    "天津",
    "河北",
    "山西",
    "内蒙古",
    "辽宁",
    "吉林",
    "黑龙江",
    "上海",
    "江苏",
    "浙江",
    "安徽",
    "福建",
    "江西",
    "山东",
    "河南",
    "湖北",
    "湖南",
    "广东",
    "广西",
    "海南",
    "重庆",
    "四川",
    "贵州",
    "云南",
    "西藏",
    "陕西",
    "甘肃",
    "青海",
    "宁夏",
    "新疆",
    "香港",
    "澳门",
    "台湾",
]

CITY_COORDS = {
    "北京": (116.407526, 39.904030),
    "天津": (117.200983, 39.084158),
    "石家庄": (114.514976, 38.042007),
    "太原": (112.548879, 37.870590),
    "呼和浩特": (111.749181, 40.842585),
    "沈阳": (123.431475, 41.805698),
    "大连": (121.614682, 38.914003),
    "长春": (125.323544, 43.817072),
    "哈尔滨": (126.534967, 45.803775),
    "上海": (121.473701, 31.230416),
    "南京": (118.796877, 32.060255),
    "苏州": (120.585315, 31.298886),
    "无锡": (120.311910, 31.491170),
    "常州": (119.974092, 31.811313),
    "杭州": (120.155070, 30.274085),
    "宁波": (121.550357, 29.874556),
    "嘉兴": (120.755486, 30.746129),
    "合肥": (117.227239, 31.820586),
    "福州": (119.296494, 26.074508),
    "厦门": (118.089425, 24.479833),
    "南昌": (115.858197, 28.682892),
    "济南": (117.120128, 36.652069),
    "青岛": (120.382639, 36.067082),
    "威海": (122.120420, 37.513068),
    "日照": (119.526888, 35.416377),
    "郑州": (113.625368, 34.746599),
    "武汉": (114.305393, 30.593099),
    "长沙": (112.938814, 28.228209),
    "广州": (113.264385, 23.129112),
    "深圳": (114.057868, 22.543099),
    "台山": (112.793812, 22.251947),
    "南宁": (108.366543, 22.817002),
    "海口": (110.198293, 20.044001),
    "重庆": (106.551643, 29.562849),
    "成都": (104.066541, 30.572269),
    "贵阳": (106.630153, 26.647661),
    "昆明": (102.832891, 24.880095),
    "拉萨": (91.140856, 29.645554),
    "西安": (108.939770, 34.341575),
    "兰州": (103.834303, 36.061089),
    "西宁": (101.778228, 36.617144),
    "银川": (106.230909, 38.487193),
    "乌鲁木齐": (87.616848, 43.825592),
    "香港": (114.169361, 22.319303),
    "澳门": (113.543873, 22.198745),
    "台北": (121.565418, 25.032969),
}


def to_int(value: float) -> int:
    if pd.isna(value):
        return 0
    return int(round(float(value)))


def to_float(value: float, digits: int = 1) -> float:
    if pd.isna(value):
        return 0.0
    return round(float(value), digits)


def min_max(series: pd.Series) -> pd.Series:
    if series.empty or series.max() == series.min():
        return pd.Series([70.0] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min()) * 100


def distribution(items: pd.Series, labels: list[str]) -> list[dict[str, int | str]]:
    counts = items.fillna("不限").replace("", "不限").value_counts()
    total = max(int(counts.sum()), 1)
    return [{"name": label, "value": int(round(counts.get(label, 0) / total * 100))} for label in labels]


def salary_distribution(df: pd.DataFrame) -> list[dict[str, int | str]]:
    bins = [
        ("6K以下", df["salary_avg"].lt(6000)),
        ("6K-10K", df["salary_avg"].ge(6000) & df["salary_avg"].lt(10000)),
        ("10K-15K", df["salary_avg"].ge(10000) & df["salary_avg"].lt(15000)),
        ("15K-25K", df["salary_avg"].ge(15000) & df["salary_avg"].lt(25000)),
        ("25K以上", df["salary_avg"].ge(25000)),
    ]
    total = max(len(df), 1)
    return [{"name": name, "value": int(round(mask.sum() / total * 100))} for name, mask in bins]


def fresh_index(group: pd.DataFrame) -> float:
    salary_df = group[group["salary_avg"].notna()]
    salary_score = 50 if salary_df.empty else min(float(salary_df["salary_avg"].mean()) / 16000 * 100, 100)
    no_exp = group["experience_norm"].eq("应届/不限").mean() * 100
    education = group["education_norm"].isin(["不限", "大专", "本科"]).mean() * 100
    return round(no_exp * 0.4 + education * 0.3 + salary_score * 0.3, 1)


def build_provinces(full_df: pd.DataFrame, salary_df: pd.DataFrame) -> list[dict]:
    salary_mean = salary_df.groupby("province")["salary_avg"].mean()
    rows = []
    real_counts = full_df["province"].value_counts()
    for province in ALL_REGIONS:
        group = full_df[full_df["province"].eq(province)]
        if group.empty:
            rows.append(
                {
                    "province": province,
                    "jobCount": 0,
                    "avgSalary": 0,
                    "freshFriendlyIndex": 0,
                    "heatIndex": 0,
                    "topIndustry": "样本不足",
                    "growthRate": 0,
                }
            )
            continue
        salary = salary_mean.get(province, pd.NA)
        top_industry = group["industry"].replace("", pd.NA).dropna().mode()
        rows.append(
            {
                "province": province,
                "jobCount": int(real_counts.get(province, 0)),
                "avgSalary": to_int(salary),
                "freshFriendlyIndex": fresh_index(group),
                "heatIndex": 0,
                "topIndustry": str(top_industry.iloc[0]) if not top_industry.empty else "未分类",
                "growthRate": 0,
            }
        )
    frame = pd.DataFrame(rows)
    positive = frame["jobCount"].gt(0)
    frame.loc[positive, "heatIndex"] = (
        min_max(frame.loc[positive, "jobCount"]) * 0.5
        + min_max(frame.loc[positive, "avgSalary"].replace(0, pd.NA).fillna(frame.loc[positive, "avgSalary"].mean())) * 0.25
        + frame.loc[positive, "freshFriendlyIndex"] * 0.25
    ).round(1)
    return frame.to_dict("records")


def build_cities(full_df: pd.DataFrame, salary_df: pd.DataFrame) -> list[dict]:
    grouped = full_df.groupby(["province", "city"], as_index=False).agg(
        jobCount=("job_title", "count"),
        freshFriendlyIndex=("experience_norm", lambda values: round(values.eq("应届/不限").mean() * 100, 1)),
    )
    salary_group = salary_df.groupby(["province", "city"], as_index=False)["salary_avg"].mean()
    grouped = grouped.merge(salary_group, on=["province", "city"], how="left")
    grouped["avgSalary"] = grouped["salary_avg"].fillna(0)
    grouped["hasCoords"] = grouped["city"].astype(str).map(lambda city: city in CITY_COORDS)
    grouped["sampleScore"] = min_max(grouped["jobCount"]).clip(0, 100)
    grouped["attractionIndex"] = (
        grouped["sampleScore"] * 0.70
        + min_max(grouped["avgSalary"].replace(0, pd.NA).fillna(grouped["avgSalary"].mean())) * 0.25
        + grouped["freshFriendlyIndex"] * 0.20
    ).round(1)
    grouped = grouped[grouped["hasCoords"]].sort_values("attractionIndex", ascending=False).head(60).reset_index(drop=True)
    rows = []
    for index, row in grouped.iterrows():
        city = str(row["city"])
        longitude, latitude = CITY_COORDS.get(city, (0, 0))
        rows.append(
            {
                "province": str(row["province"]),
                "city": city,
                "jobCount": to_int(row["jobCount"]),
                "avgSalary": to_int(row["avgSalary"]),
                "freshFriendlyIndex": to_float(row["freshFriendlyIndex"]),
                "attractionIndex": to_float(row["attractionIndex"]),
                "rankNo": index + 1,
                "longitude": longitude,
                "latitude": latitude,
            }
        )
    return rows


def build_trend(full_df: pd.DataFrame) -> list[dict]:
    valid = full_df.dropna(subset=["publish_date"]).copy()
    if valid.empty:
        return []
    valid["month"] = valid["publish_date"].dt.to_period("M").astype(str)
    ai_pattern = r"(?i)(?:\bAI\b|artificial intelligence|人工智能|机器学习|深度学习|算法)"
    valid["is_ai"] = valid["text"].str.contains(ai_pattern, regex=True, na=False)
    grouped = valid.groupby("month")
    rows = []
    for month, group in grouped:
        rows.append(
            {
                "month": month,
                "jobs": int(len(group)),
                "freshJobs": int(group["experience_norm"].eq("应届/不限").sum()),
                "aiJobs": int(group["is_ai"].sum()),
            }
        )
    return rows[-12:]


def build_hot_industries(full_df: pd.DataFrame) -> list[dict]:
    grouped = full_df.groupby("industry", as_index=False).agg(value=("job_title", "count"))
    grouped = grouped[grouped["industry"].astype(str).str.strip().ne("")]
    grouped = grouped.sort_values("value", ascending=False).head(10).reset_index(drop=True)
    max_value = max(int(grouped["value"].max()), 1) if not grouped.empty else 1
    return [
        {"name": str(row["industry"]), "value": int(row["value"]), "score": round(int(row["value"]) / max_value * 100, 1), "tag": "真实样本"}
        for _, row in grouped.iterrows()
    ]


def build_skills(full_df: pd.DataFrame) -> list[dict]:
    skill_counts: dict[str, dict[str, object]] = {}
    for _, row in full_df.iterrows():
        skills = extract_skills(str(row["text"]))
        for skill in skills:
            item = skill_counts.setdefault(skill, {"frequency": 0, "categories": []})
            item["frequency"] = int(item["frequency"]) + 1
            item["categories"].append(str(row["job_category"]))
    rows = []
    max_frequency = max([int(item["frequency"]) for item in skill_counts.values()] or [1])
    for skill, item in skill_counts.items():
        categories = pd.Series(item["categories"])
        category = categories.mode().iloc[0] if not categories.mode().empty else "综合岗位"
        frequency = int(item["frequency"])
        heat = round(frequency / max_frequency * 100, 1)
        rows.append({"skill": skill, "frequency": frequency, "heatIndex": heat, "category": category, "trendScore": heat})
    return sorted(rows, key=lambda item: item["heatIndex"], reverse=True)[:36]


def build_live_jobs(full_df: pd.DataFrame) -> list[dict]:
    latest = full_df.sort_values("publish_date", ascending=False).head(10)
    rows = []
    for _, row in latest.iterrows():
        salary = str(row.get("salary_text", "") or "").replace("/月", "")
        if not salary and pd.notna(row.get("salary_avg")):
            salary = f"{to_int(row['salary_avg'])}元"
        skills = row.get("skill_text", "") or row.get("industry", "")
        rows.append(
            {
                "time": str(row["publish_date"].date()) if pd.notna(row["publish_date"]) else "未知日期",
                "city": str(row["city"]),
                "title": str(row["job_title"])[:28],
                "company": str(row["company_name"])[:24] or str(row["source_dataset"]),
                "salary": salary or "未公开",
                "skills": str(skills).replace(",", " / ")[:42],
            }
        )
    return rows


def write_backend(provinces, cities, overview, analysis, live_jobs) -> None:
    payload = {
        "PROVINCE_METRICS": provinces,
        "CITY_METRICS": cities,
        "OVERVIEW": overview,
        "ANALYSIS": analysis,
        "LIVE_JOBS": live_jobs,
    }
    code = '''from app.schemas import (
    CityMetric,
    DashboardAnalysis,
    DashboardOverview,
    JobLiveItem,
    ProvinceMetric,
)

# Generated from real Kaggle and China Public Recruitment Network data.
DATA = __DATA__


def province_metrics() -> list[ProvinceMetric]:
    return [ProvinceMetric(**item) for item in DATA["PROVINCE_METRICS"]]


def city_metrics() -> list[CityMetric]:
    return [CityMetric(**item) for item in DATA["CITY_METRICS"]]


def dashboard_overview() -> DashboardOverview:
    return DashboardOverview(**DATA["OVERVIEW"])


def dashboard_analysis() -> DashboardAnalysis:
    return DashboardAnalysis(**DATA["ANALYSIS"])


def live_jobs() -> list[JobLiveItem]:
    return [JobLiveItem(**item) for item in DATA["LIVE_JOBS"]]
'''
    BACKEND_DATA.write_text(code.replace("__DATA__", repr(payload)), encoding="utf-8")


def write_frontend(provinces, cities, overview, analysis, live_jobs) -> None:
    text = f"""import type {{
  CareerRecommendation,
  CityMetric,
  DashboardAnalysis,
  DashboardOverview,
  JobLiveItem,
  ProvinceMetric,
  SalaryPrediction
}} from '../types/dashboard'

// Generated from real Kaggle and China Public Recruitment Network data.
export const provinceMetrics: ProvinceMetric[] = {json.dumps(provinces, ensure_ascii=False, indent=2)}

export const cityMetrics: CityMetric[] = {json.dumps(cities, ensure_ascii=False, indent=2)}

export const overview: DashboardOverview = {json.dumps(overview, ensure_ascii=False, indent=2)}

export const analysis: DashboardAnalysis = {json.dumps(analysis, ensure_ascii=False, indent=2)}

export const liveJobs: JobLiveItem[] = {json.dumps(live_jobs, ensure_ascii=False, indent=2)}

export const mockSalaryPrediction: SalaryPrediction = {{
  predictedMin: Math.round(overview.averageSalary * 0.82),
  predictedMax: Math.round(overview.averageSalary * 1.24),
  predictedAvg: overview.averageSalary,
  confidence: 72.5,
  modelName: 'RealDataBaseline',
  explanation: '基于真实岗位样本平均薪资生成的前端兜底预测；后端可接入 data-processing 输出的模型文件。',
  influenceFactors: ['真实样本平均薪资', '城市岗位样本', '行业样本', '学历经验分布', '技能文本']
}}

export const mockRecommendations: CareerRecommendation[] = [
  {{
    direction: '生产制造与设备操作方向',
    city: cityMetrics[0]?.city ?? '西安',
    industry: '生产制造及有关人员',
    jobCategory: '生产制造与设备操作',
    matchScore: 82,
    salaryPotential: overview.averageSalary,
    reason: '根据最新真实样本中的城市、行业和技能热度生成兜底推荐。',
    skillGaps: ['安全', '质量', '机械'],
    suggestions: ['优先选择真实样本岗位数较高的城市', '补齐安全、质量和设备基础', '投递前核对目标岗位薪资是否公开']
  }}
]
"""
    FRONTEND_DATA.write_text(text, encoding="utf-8")


def main() -> None:
    full_df = clean_jobs_for_coverage(DATA_INPUT)
    salary_values = full_df["salary_text"].apply(parse_salary)
    full_df[["salary_min", "salary_max", "salary_avg"]] = pd.DataFrame(salary_values.tolist(), index=full_df.index)
    salary_df = full_df[full_df["salary_avg"].notna() & full_df["salary_avg"].between(1000, 100000)].copy()

    provinces = build_provinces(full_df, salary_df)
    cities = build_cities(full_df, salary_df)
    trend = build_trend(full_df)
    hot_cities = [
        {"name": item["city"], "value": item["jobCount"], "score": item["attractionIndex"], "tag": item["province"]}
        for item in cities[:10]
    ]
    total_jobs = int(len(full_df))
    average_salary = to_int(salary_df["salary_avg"].mean()) if not salary_df.empty else 0
    overview = {
        "totalJobs": total_jobs,
        "averageSalary": average_salary,
        "coveredCities": int(full_df["city"].nunique()),
        "freshFriendlyIndex": round(full_df["experience_norm"].eq("应届/不限").mean() * 100, 1),
        "hotCities": hot_cities,
        "hotIndustries": build_hot_industries(full_df),
        "monthlyTrend": trend,
    }
    analysis = {
        "salaryRanges": salary_distribution(salary_df),
        "education": distribution(full_df["education_norm"], ["不限", "大专", "本科", "硕士", "博士"]),
        "experience": distribution(full_df["experience_norm"], ["应届/不限", "1-3年", "3-5年", "5年以上"]),
        "skills": build_skills(full_df),
    }
    live_jobs = build_live_jobs(full_df)
    write_backend(provinces, cities, overview, analysis, live_jobs)
    write_frontend(provinces, cities, overview, analysis, live_jobs)

    metadata = {
        "rows": total_jobs,
        "salary_rows": int(len(salary_df)),
        "covered_regions_with_samples": int(sum(1 for item in provinces if item["jobCount"] > 0)),
        "regions_without_samples": [item["province"] for item in provinces if item["jobCount"] == 0],
        "covered_cities": overview["coveredCities"],
        "average_salary": average_salary,
    }
    SNAPSHOT_META.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
