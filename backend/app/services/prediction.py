from app.schemas import SalaryPrediction, SalaryPredictionRequest


CITY_BASE = {
    "北京": 19000,
    "上海": 18200,
    "深圳": 18600,
    "杭州": 16800,
    "广州": 15100,
    "南京": 13900,
    "成都": 12600,
    "武汉": 11900,
}


def factor(source: str, rules: list[tuple[str, float]]) -> float:
    for keyword, value in rules:
        if keyword in source:
            return value
    return 1.0


def predict_salary(payload: SalaryPredictionRequest) -> SalaryPrediction:
    base = CITY_BASE.get(payload.city, 11000)
    industry_factor = factor(payload.industry, [("人工智能", 1.22), ("金融科技", 1.15), ("互联网", 1.10)])
    education_factor = factor(payload.education, [("博士", 1.35), ("硕士", 1.18), ("本科", 1.0)])
    experience_factor = factor(payload.experience, [("5年以上", 1.45), ("3-5年", 1.28), ("1-3年", 1.10)])
    category_factor = factor(payload.jobCategory, [("算法", 1.25), ("数据", 1.12), ("后端", 1.08)])
    skill_factor = 1.05 if "Python" in payload.skills else 1.0

    predicted_avg = round(base * industry_factor * education_factor * experience_factor * category_factor * skill_factor)
    predicted_min = round(predicted_avg * 0.82)
    predicted_max = round(predicted_avg * 1.24)

    return SalaryPrediction(
        predictedMin=predicted_min,
        predictedMax=predicted_max,
        predictedAvg=predicted_avg,
        confidence=86.5,
        modelName="RandomForestRegressor",
        explanation="演示服务按城市、行业、学历、经验、岗位类别和技能因子估算薪资；真实部署时由 data-processing 训练模型文件提供预测。",
        influenceFactors=[
            f"城市薪资基准：{payload.city}",
            f"行业溢价：{payload.industry}",
            f"学历门槛：{payload.education}",
            f"经验要求：{payload.experience}",
            f"岗位类别：{payload.jobCategory}",
        ],
    )
