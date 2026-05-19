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
    cities = payload.expectedCities or ["深圳", "杭州", "成都"]
    industries = payload.expectedIndustries or ["互联网/电子商务", "软件服务", "人工智能"]

    return [
        CareerRecommendation(
            direction="数据分析与商业智能方向",
            city=at(cities, 0, "深圳"),
            industry=at(industries, 0, "互联网/电子商务"),
            jobCategory="数据分析师",
            matchScore=cap(78 + (8 if contains(skills, "SQL") else 0) + (8 if contains(skills, "Python") else 0)),
            salaryPotential=16000,
            reason=f"该方向与{payload.major}专业的数据处理、指标分析和业务理解能力匹配，就业城市岗位密度较高。",
            skillGaps=gaps(skills, ["SQL", "Python", "可视化", "统计分析"]),
            suggestions=["补强 SQL 窗口函数和复杂查询", "完成 1 个行业数据分析作品集", "学习 ECharts 或 BI 工具表达分析结论"],
        ),
        CareerRecommendation(
            direction="企业级软件开发方向",
            city=at(cities, 1, "杭州"),
            industry=at(industries, 1, "软件服务"),
            jobCategory="后端/全栈开发工程师",
            matchScore=cap(74 + (10 if contains(skills, "Python") else 0) + (5 if contains(skills, "Vue") else 0)),
            salaryPotential=18000,
            reason="软件服务行业对应届本科生吸纳稳定，岗位体系清晰，适合通过项目经验提升竞争力。",
            skillGaps=gaps(skills, ["Python", "FastAPI", "MySQL", "Redis"]),
            suggestions=["完成 Python FastAPI + MySQL 项目闭环", "补齐缓存、接口鉴权和部署经验", "准备接口设计与数据库设计答辩材料"],
        ),
        CareerRecommendation(
            direction="人工智能与算法应用方向",
            city=at(cities, 2, "北京"),
            industry=at(industries, 2, "人工智能"),
            jobCategory="算法应用工程师",
            matchScore=cap(68 + (8 if contains(skills, "Python") else 0) + (12 if contains(skills, "机器学习") or contains(skills, "人工智能") else 0)),
            salaryPotential=23000,
            reason="人工智能岗位薪资潜力高，但学历和项目门槛更高，适合作为冲刺方向或读研深造方向。",
            skillGaps=gaps(skills, ["Python", "机器学习", "深度学习", "模型评估"]),
            suggestions=["补充机器学习基础模型和评价指标", "完成一个可复现实验项目", "关注算法应用岗而非纯研究岗，降低进入门槛"],
        ),
    ]
