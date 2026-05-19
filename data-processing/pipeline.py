import argparse
import json
import re
from pathlib import Path

import jieba
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


FIELD_ALIASES = {
    "job_title": ["job_title", "title", "岗位名称", "职位名称", "position"],
    "company_name": ["company_name", "company", "公司名称", "企业名称"],
    "city": ["city", "work_city", "工作城市", "城市"],
    "province": ["province", "work_province", "工作省份", "省份"],
    "salary_text": ["salary", "salary_range", "薪资", "薪资范围"],
    "education": ["education", "学历要求", "学历"],
    "experience": ["experience", "经验要求", "工作经验"],
    "industry": ["industry", "行业", "行业类别"],
    "major": ["major", "专业要求", "专业"],
    "company_size": ["company_size", "公司规模", "规模"],
    "company_type": ["company_type", "公司性质", "企业性质"],
    "publish_date": ["publish_date", "发布时间", "发布日期", "date"],
    "description": ["description", "job_description", "岗位描述", "职位描述"],
    "longitude": ["longitude", "lng", "经度"],
    "latitude": ["latitude", "lat", "纬度"],
}

PROVINCE_BY_CITY = {
    "北京": "北京",
    "上海": "上海",
    "深圳": "广东",
    "广州": "广东",
    "杭州": "浙江",
    "南京": "江苏",
    "成都": "四川",
    "武汉": "湖北",
    "西安": "陕西",
    "青岛": "山东",
    "重庆": "重庆",
    "厦门": "福建",
    "郑州": "河南",
}

SKILL_LEXICON = [
    "FastAPI",
    "Python",
    "SQL",
    "MySQL",
    "Redis",
    "Vue",
    "TypeScript",
    "ECharts",
    "大数据",
    "Spark",
    "Hive",
    "Flink",
    "人工智能",
    "机器学习",
    "深度学习",
    "数据分析",
    "前端开发",
    "后端开发",
    "云计算",
    "Linux",
    "PyTorch",
]


def pick_column(df: pd.DataFrame, aliases: list[str]) -> pd.Series:
    for name in aliases:
        if name in df.columns:
            return df[name]
    return pd.Series([""] * len(df))


def normalize_columns(raw: pd.DataFrame) -> pd.DataFrame:
    data = {target: pick_column(raw, aliases) for target, aliases in FIELD_ALIASES.items()}
    df = pd.DataFrame(data)
    for column in ["job_title", "company_name", "city", "province", "education", "experience", "industry", "major", "company_size", "company_type", "description"]:
        df[column] = df[column].fillna("").astype(str).str.strip()
    df["city"] = df["city"].str.replace("市", "", regex=False)
    df["province"] = df.apply(lambda row: row["province"] or PROVINCE_BY_CITY.get(row["city"], "未知"), axis=1)
    df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")
    return df


def parse_salary(text: str) -> tuple[float, float, float]:
    if not isinstance(text, str) or not text.strip():
        return np.nan, np.nan, np.nan

    source = text.lower().replace(" ", "")
    multiplier = 1.0
    if "万/年" in source or "w/年" in source:
        multiplier = 10000 / 12
    elif "k" in source or "千" in source:
        multiplier = 1000
    elif "万" in source:
        multiplier = 10000

    numbers = [float(item) for item in re.findall(r"\d+(?:\.\d+)?", source)]
    if not numbers:
        return np.nan, np.nan, np.nan
    if len(numbers) == 1:
        low = high = numbers[0] * multiplier
    else:
        low, high = numbers[0] * multiplier, numbers[1] * multiplier
    avg = (low + high) / 2
    return round(low, 2), round(high, 2), round(avg, 2)


def normalize_education(value: str) -> str:
    if "博士" in value:
        return "博士"
    if "硕士" in value or "研究生" in value:
        return "硕士"
    if "本科" in value:
        return "本科"
    if "大专" in value or "专科" in value:
        return "大专"
    return "不限"


def normalize_experience(value: str) -> str:
    if "应届" in value or "不限" in value or not value:
        return "应届/不限"
    if "5" in value or "五" in value:
        return "5年以上"
    if "3" in value:
        return "3-5年"
    return "1-3年"


def extract_job_category(title: str) -> str:
    if any(key in title for key in ["算法", "机器学习", "人工智能"]):
        return "算法工程师"
    if any(key in title for key in ["数据分析", "BI", "商业分析"]):
        return "数据分析"
    if any(key in title for key in ["大数据", "数仓", "数据开发"]):
        return "数据开发"
    if any(key in title for key in ["前端", "Vue", "React"]):
        return "前端开发"
    if any(key in title for key in ["Python", "FastAPI", "后端", "服务端"]):
        return "后端开发"
    return "综合岗位"


def extract_skills(text: str) -> list[str]:
    lower_text = text.lower()
    found = []
    for skill in SKILL_LEXICON:
        if skill.lower() in lower_text or skill in text:
            found.append(skill)
    return sorted(set(found))


def clean_jobs(input_path: Path) -> pd.DataFrame:
    raw = pd.read_csv(input_path)
    df = normalize_columns(raw)
    salary_values = df["salary_text"].apply(parse_salary)
    df[["salary_min", "salary_max", "salary_avg"]] = pd.DataFrame(salary_values.tolist(), index=df.index)
    df["education_norm"] = df["education"].apply(normalize_education)
    df["experience_norm"] = df["experience"].apply(normalize_experience)
    df["job_category"] = df["job_title"].apply(extract_job_category)
    df["text"] = (df["job_title"] + " " + df["description"]).fillna("")
    df["skills"] = df["text"].apply(extract_skills)
    df["skill_text"] = df["skills"].apply(lambda values: ",".join(values))
    df = df[df["city"].ne("")]
    df = df[df["salary_avg"].notna()]
    df = df[df["salary_avg"].between(1000, 100000)]
    return df


def min_max(series: pd.Series) -> pd.Series:
    if series.max() == series.min():
        return pd.Series([100.0] * len(series), index=series.index)
    return (series - series.min()) / (series.max() - series.min()) * 100


def fresh_friendly(group: pd.DataFrame) -> float:
    no_exp = group["experience_norm"].eq("应届/不限").mean() * 100
    bachelor = group["education_norm"].isin(["不限", "大专", "本科"]).mean() * 100
    salary_score = min(group["salary_avg"].mean() / 20000 * 100, 100)
    return round(no_exp * 0.35 + bachelor * 0.25 + salary_score * 0.25 + 75 * 0.15, 2)


def build_city_index(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(["province", "city"], as_index=False).agg(
        job_count=("job_title", "count"),
        avg_salary=("salary_avg", "mean"),
        industry_diversity=("industry", "nunique"),
    )
    fresh = df.groupby(["province", "city"]).apply(fresh_friendly, include_groups=False).reset_index(name="fresh_friendly_index")
    result = grouped.merge(fresh, on=["province", "city"], how="left")
    result["education_threshold_index"] = 100 - df.groupby(["province", "city"])["education_norm"].apply(
        lambda values: values.isin(["硕士", "博士"]).mean() * 100
    ).reset_index(drop=True)
    result["experience_threshold_index"] = 100 - df.groupby(["province", "city"])["experience_norm"].apply(
        lambda values: values.isin(["3-5年", "5年以上"]).mean() * 100
    ).reset_index(drop=True)
    result["city_attraction_index"] = (
        min_max(result["job_count"]) * 0.25
        + min_max(result["avg_salary"]) * 0.25
        + result["fresh_friendly_index"] * 0.20
        + min_max(result["industry_diversity"]) * 0.15
        + result["education_threshold_index"] * 0.08
        + result["experience_threshold_index"] * 0.07
    ).round(2)
    result["rank_no"] = result["city_attraction_index"].rank(method="first", ascending=False).astype(int)
    return result.sort_values("rank_no")


def build_province_index(df: pd.DataFrame, city_index: pd.DataFrame) -> pd.DataFrame:
    result = df.groupby("province", as_index=False).agg(
        job_count=("job_title", "count"),
        avg_salary=("salary_avg", "mean"),
        top_industry=("industry", lambda values: values.mode().iloc[0] if not values.mode().empty else "未知"),
    )
    fresh = city_index.groupby("province", as_index=False)["fresh_friendly_index"].mean()
    result = result.merge(fresh, on="province", how="left")
    result["employment_heat_index"] = (
        min_max(result["job_count"]) * 0.45
        + min_max(result["avg_salary"]) * 0.30
        + result["fresh_friendly_index"] * 0.25
    ).round(2)
    result["growth_rate"] = np.random.default_rng(42).uniform(3, 14, len(result)).round(2)
    return result.sort_values("employment_heat_index", ascending=False)


def tokenize(text: str) -> str:
    return " ".join(word for word in jieba.lcut(text) if len(word.strip()) > 1)


def build_skill_keywords(df: pd.DataFrame) -> pd.DataFrame:
    corpus = df["text"].fillna("").apply(tokenize)
    vectorizer = TfidfVectorizer(max_features=200)
    tfidf = vectorizer.fit_transform(corpus)
    feature_names = np.array(vectorizer.get_feature_names_out())
    tfidf_scores = np.asarray(tfidf.mean(axis=0)).ravel()
    tfidf_map = dict(zip(feature_names, tfidf_scores))

    rows = []
    for skill in SKILL_LEXICON:
        mask = df["skill_text"].str.contains(re.escape(skill), case=False, na=False)
        frequency = int(mask.sum())
        if frequency == 0:
            continue
        rows.append(
            {
                "skill_name": skill,
                "job_category": df.loc[mask, "job_category"].mode().iloc[0],
                "industry": df.loc[mask, "industry"].mode().iloc[0] if not df.loc[mask, "industry"].mode().empty else "未知",
                "frequency_count": frequency,
                "tfidf_weight": round(float(tfidf_map.get(skill.lower(), tfidf_map.get(skill, 0.0))), 6),
                "textrank_weight": round(min(frequency / max(len(df), 1), 1), 6),
                "trend_score": round(min(60 + frequency / max(len(df), 1) * 60, 100), 2),
            }
        )
    result = pd.DataFrame(rows)
    if result.empty:
        return result
    result["heat_index"] = (
        min_max(result["frequency_count"]) * 0.45
        + min_max(result["tfidf_weight"]) * 0.30
        + min_max(result["textrank_weight"]) * 0.15
        + result["trend_score"] * 0.10
    ).round(2)
    return result.sort_values("heat_index", ascending=False)


def train_salary_model(df: pd.DataFrame, output_dir: Path) -> dict:
    features = ["city", "province", "industry", "education_norm", "experience_norm", "company_size", "company_type", "job_category"]
    train_df = df.dropna(subset=["salary_avg"]).copy()
    x = train_df[features]
    y = train_df["salary_avg"]

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(transformers=[("category", categorical_pipeline, features)])
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=160, random_state=42, min_samples_leaf=2)),
        ]
    )

    if len(train_df) < 10:
        model.fit(x, y)
        metrics = {"mae": None, "rmse": None, "r2": None, "note": "样本少于10条，仅训练演示模型"}
    else:
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        model.fit(x_train, y_train)
        prediction = model.predict(x_test)
        metrics = {
            "mae": round(float(mean_absolute_error(y_test, prediction)), 2),
            "rmse": round(float(mean_squared_error(y_test, prediction, squared=False)), 2),
            "r2": round(float(r2_score(y_test, prediction)), 4),
        }

    joblib.dump(model, output_dir / "salary_model.joblib")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="中国招聘岗位数据处理与模型训练")
    parser.add_argument("--input", required=True, type=Path, help="Kaggle CSV 输入文件")
    parser.add_argument("--output", required=True, type=Path, help="输出目录")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    clean_df = clean_jobs(args.input)
    city_index = build_city_index(clean_df)
    province_index = build_province_index(clean_df, city_index)
    skill_keywords = build_skill_keywords(clean_df)
    metrics = train_salary_model(clean_df, args.output)

    clean_df.to_csv(args.output / "clean_jobs.csv", index=False, encoding="utf-8-sig")
    city_index.to_csv(args.output / "city_index.csv", index=False, encoding="utf-8-sig")
    province_index.to_csv(args.output / "province_index.csv", index=False, encoding="utf-8-sig")
    skill_keywords.to_csv(args.output / "skill_keywords.csv", index=False, encoding="utf-8-sig")
    (args.output / "model_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"rows": len(clean_df), "metrics": metrics}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
