from app.schemas import CareerRecommendation, CareerRecommendationRequest
from app.services.ai_client import request_ai_json


CAREER_AI_PROMPT = """
你是高校就业指导顾问。请基于真实招聘快照形成的本地基线推荐和学生画像，
输出 3 个职业路径推荐。必须只输出 JSON 数组，不要 Markdown，不要解释。

每个数组元素必须包含：
direction, city, industry, jobCategory, matchScore, salaryPotential,
reason, skillGaps, suggestions。

约束：
- matchScore 是 0 到 98 的数字。
- salaryPotential 是月薪整数，单位为人民币元。
- reason 用 1 句中文说明推荐依据，80 字以内。
- skillGaps 最多 4 项。
- suggestions 必须是 3 条可执行建议，每条 30 字以内。
- 优先使用用户期望城市、期望行业和本地基线推荐，不要编造具体公司。
""".strip()


def contains(skills: list[str], target: str) -> bool:
    return any(skill.lower() == target.lower() or target in skill for skill in skills)


def gaps(skills: list[str], required: list[str]) -> list[str]:
    return [skill for skill in required if not contains(skills, skill)]


def cap(value: float) -> float:
    return min(value, 98.0)


def at(values: list[str], index: int, fallback: str) -> str:
    return values[index] if len(values) > index else fallback


def recommend_career(payload: CareerRecommendationRequest) -> list[CareerRecommendation]:
    skills = payload.skills or []
    cities = payload.expectedCities or ["西安", "重庆", "苏州"]
    industries = payload.expectedIndustries or ["生产制造及有关人员", "专业技术人员", "销售人员"]

    return [
        CareerRecommendation(
            direction="生产制造与设备操作方向",
            city=at(cities, 0, "西安"),
            industry=at(industries, 0, "生产制造及有关人员"),
            jobCategory="生产制造与设备操作",
            matchScore=cap(78 + (8 if contains(skills, "生产") else 0) + (6 if contains(skills, "安全") else 0) + (6 if contains(skills, "质量") else 0)),
            salaryPotential=6200,
            reason=f"最新真实岗位样本中生产制造、设备操作和质量相关岗位占比较高，适合{payload.major}等应用型专业优先投递。",
            skillGaps=gaps(skills, ["生产", "安全", "质量", "机械"]),
            suggestions=["补充安全生产和质量管理基础", "整理实训或生产现场经历", "优先投递岗位样本较多的城市"],
        ),
        CareerRecommendation(
            direction="销售与客户服务方向",
            city=at(cities, 1, "重庆"),
            industry=at(industries, 1, "销售人员"),
            jobCategory="销售/客户服务",
            matchScore=cap(74 + (8 if contains(skills, "销售") else 0) + (8 if contains(skills, "沟通") else 0) + (4 if contains(skills, "Office") else 0)),
            salaryPotential=5600,
            reason="销售、客户服务和生活服务类岗位在公开招聘样本中数量稳定，适合作为毕业生保底和转岗方向。",
            skillGaps=gaps(skills, ["销售", "沟通", "客户服务", "Office"]),
            suggestions=["准备客户沟通和跟进案例", "补齐 Office 与基础数据记录能力", "投递时关注底薪、提成和社保口径"],
        ),
        CareerRecommendation(
            direction="机械电气与财务运营方向",
            city=at(cities, 2, "苏州"),
            industry=at(industries, 2, "专业技术人员"),
            jobCategory="机械/电气/财务运营",
            matchScore=cap(70 + (8 if contains(skills, "机械") else 0) + (8 if contains(skills, "电气") else 0) + (5 if contains(skills, "Excel") or contains(skills, "会计") else 0)),
            salaryPotential=7000,
            reason="机械、电气、会计、采购、仓储等词在真实样本中持续出现，适合作为专业技术或职能支持方向。",
            skillGaps=gaps(skills, ["机械", "电气", "Excel", "会计"]),
            suggestions=["根据专业选择机械电气或财务运营分支", "准备证书、实训或报表作品", "优先核对岗位薪资、学历和经验要求"],
        ),
    ]


def recommend_career_with_ai(payload: CareerRecommendationRequest) -> list[CareerRecommendation]:
    baseline = recommend_career(payload)
    ai_data = request_ai_json(
        CAREER_AI_PROMPT,
        {
            "studentProfile": payload.model_dump(),
            "baselineRecommendations": [item.model_dump() for item in baseline],
        },
    )
    return normalize_ai_recommendations(ai_data, baseline) or baseline


def normalize_ai_recommendations(
    ai_data: object,
    baseline: list[CareerRecommendation],
) -> list[CareerRecommendation]:
    if isinstance(ai_data, dict):
        ai_data = ai_data.get("recommendations") or ai_data.get("items") or ai_data.get("data")
    if not isinstance(ai_data, list):
        return []

    recommendations: list[CareerRecommendation] = []
    for index, item in enumerate(ai_data[:3]):
        if not isinstance(item, dict):
            continue
        fallback = baseline[min(index, len(baseline) - 1)]
        try:
            recommendations.append(
                CareerRecommendation(
                    direction=text_value(item.get("direction"), fallback.direction, 36),
                    city=text_value(item.get("city"), fallback.city, 20),
                    industry=text_value(item.get("industry"), fallback.industry, 60),
                    jobCategory=text_value(item.get("jobCategory"), fallback.jobCategory, 50),
                    matchScore=bounded_float(item.get("matchScore"), fallback.matchScore, 0, 98),
                    salaryPotential=bounded_int(item.get("salaryPotential"), fallback.salaryPotential, 2500, 50000),
                    reason=text_value(item.get("reason"), fallback.reason, 120),
                    skillGaps=text_list(item.get("skillGaps"), fallback.skillGaps, 4, 20),
                    suggestions=text_list(item.get("suggestions"), fallback.suggestions, 3, 30),
                )
            )
        except (TypeError, ValueError):
            continue

    existing_directions = {item.direction for item in recommendations}
    for fallback in baseline:
        if len(recommendations) >= 3:
            break
        if fallback.direction not in existing_directions:
            recommendations.append(fallback)
    return recommendations[:3]


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


def bounded_float(value: object, fallback: float, floor: float, ceiling: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = fallback
    return round(min(max(number, floor), ceiling), 1)


def bounded_int(value: object, fallback: int, floor: int, ceiling: int) -> int:
    try:
        number = int(float(value))
    except (TypeError, ValueError):
        number = fallback
    return min(max(number, floor), ceiling)
