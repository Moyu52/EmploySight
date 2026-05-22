from app.schemas import SalaryPrediction, SalaryPredictionRequest
from app.services.ai_client import request_ai_json
from app.services.demo_data import DATA


CITY_BASE = {
    item["city"]: item["avgSalary"]
    for item in DATA["CITY_METRICS"]
    if item.get("avgSalary", 0) > 0
}
DEFAULT_AVERAGE_SALARY = DATA["OVERVIEW"]["averageSalary"]
SALARY_AI_PROMPT = """
你是高校就业数据分析顾问。请基于学生输入和后端薪资模型给出的基线预测，
生成面向毕业生的薪资解释。必须只输出 JSON 对象，不要 Markdown，不要解释。

JSON 字段：
- explanation: 1 段中文，120 字以内，解释预测区间和风险。
- influenceFactors: 4 到 6 条中文要点，每条 35 字以内。

约束：
- 不要修改 predictedMin、predictedMax、predictedAvg。
- 不要编造具体公司、岗位数量或不存在的数据来源。
- 保持措辞审慎，说明这是投递前的参考，不是薪资承诺。
""".strip()


def factor(source: str, rules: list[tuple[str, float]]) -> float:
    for keyword, value in rules:
        if keyword in source:
            return value
    return 1.0


def predict_salary(payload: SalaryPredictionRequest) -> SalaryPrediction:
    base = CITY_BASE.get(payload.city, DEFAULT_AVERAGE_SALARY)
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


def predict_salary_with_ai(payload: SalaryPredictionRequest) -> SalaryPrediction:
    baseline = predict_salary(payload)
    ai_data = request_ai_json(
        SALARY_AI_PROMPT,
        {
            "salaryInput": payload.model_dump(),
            "baselinePrediction": baseline.model_dump(),
        },
    )
    return apply_ai_salary_analysis(ai_data, baseline)


def apply_ai_salary_analysis(ai_data: object, baseline: SalaryPrediction) -> SalaryPrediction:
    if not isinstance(ai_data, dict):
        return baseline

    explanation = text_value(ai_data.get("explanation"), baseline.explanation, 150)
    factors = text_list(ai_data.get("influenceFactors"), baseline.influenceFactors, 6, 40)
    if explanation == baseline.explanation and factors == baseline.influenceFactors:
        return baseline

    return baseline.model_copy(
        update={
            "modelName": f"{baseline.modelName}+AIInsight",
            "explanation": explanation,
            "influenceFactors": factors,
        }
    )


def text_value(value: object, fallback: str, max_length: int) -> str:
    text = str(value).strip() if value is not None else ""
    return (text or fallback)[:max_length]


def text_list(value: object, fallback: list[str], limit: int, max_length: int) -> list[str]:
    if isinstance(value, list):
        items = [str(item).strip()[:max_length] for item in value if str(item).strip()]
    elif isinstance(value, str):
        items = [item.strip()[:max_length] for item in value.replace("；", ";").split(";") if item.strip()]
    else:
        items = []

    result = items[:limit]
    for item in fallback:
        if len(result) >= limit:
            break
        if item not in result:
            result.append(item[:max_length])
    return result
