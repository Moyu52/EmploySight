from app.schemas import SalaryPrediction, SalaryPredictionRequest


CITY_BASE = {
    "北京": 11869,
    "上海": 14004,
    "深圳": 9160,
    "广州": 20040,
    "南京": 9633,
    "苏州": 6972,
    "常州": 7077,
    "重庆": 5643,
    "西安": 4710,
    "哈尔滨": 5543,
    "长春": 6023,
    "大连": 4535,
    "西宁": 5447,
    "青岛": 5144,
    "武汉": 7529,
}


def factor(source: str, rules: list[tuple[str, float]]) -> float:
    for keyword, value in rules:
        if keyword in source:
            return value
    return 1.0


def predict_salary(payload: SalaryPredictionRequest) -> SalaryPrediction:
    base = CITY_BASE.get(payload.city, 5681)
    industry_factor = factor(
        payload.industry,
        [
            ("专业技术", 1.12),
            ("机械", 1.08),
            ("电气", 1.08),
            ("生产制造", 1.02),
            ("销售", 1.00),
            ("服务", 0.96),
        ],
    )
    education_factor = factor(payload.education, [("博士", 1.30), ("硕士", 1.18), ("本科", 1.08), ("大专", 1.0)])
    experience_factor = factor(payload.experience, [("5年以上", 1.28), ("3-5年", 1.15), ("1-3年", 1.06)])
    category_factor = factor(
        payload.jobCategory,
        [
            ("质量", 1.08),
            ("设备", 1.06),
            ("机械", 1.06),
            ("电气", 1.06),
            ("财务", 1.04),
            ("销售", 1.00),
        ],
    )
    skill_factor = 1.04 if any(skill in payload.skills for skill in ["质量", "安全", "电气", "机械", "Excel"]) else 1.0

    predicted_avg = round(base * industry_factor * education_factor * experience_factor * category_factor * skill_factor)
    predicted_min = round(predicted_avg * 0.82)
    predicted_max = round(predicted_avg * 1.24)

    return SalaryPrediction(
        predictedMin=predicted_min,
        predictedMax=predicted_max,
        predictedAvg=predicted_avg,
        confidence=82.0,
        modelName="RealDataHeuristic",
        explanation="按最新真实岗位快照的城市薪资基准、行业、学历、经验、岗位类别和技能因子估算薪资；训练指标见 data-processing/output/model_metrics.json。",
        influenceFactors=[
            f"城市薪资基准：{payload.city}",
            f"行业结构：{payload.industry}",
            f"学历门槛：{payload.education}",
            f"经验要求：{payload.experience}",
            f"岗位类别：{payload.jobCategory}",
        ],
    )
