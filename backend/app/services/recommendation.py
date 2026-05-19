from app.schemas import CareerRecommendation, CareerRecommendationRequest


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
