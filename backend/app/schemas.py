from typing import Any

from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any


class RankItem(BaseModel):
    name: str
    value: float
    score: float
    tag: str


class TrendPoint(BaseModel):
    month: str
    jobs: int
    freshJobs: int
    aiJobs: int


class DashboardOverview(BaseModel):
    totalJobs: int
    averageSalary: float
    coveredCities: int
    freshFriendlyIndex: float
    hotCities: list[RankItem]
    hotIndustries: list[RankItem]
    monthlyTrend: list[TrendPoint]


class ProvinceMetric(BaseModel):
    province: str
    jobCount: int
    avgSalary: float
    freshFriendlyIndex: float
    heatIndex: float
    topIndustry: str
    growthRate: float


class CityMetric(BaseModel):
    province: str
    city: str
    jobCount: int
    avgSalary: float
    freshFriendlyIndex: float
    attractionIndex: float
    rankNo: int
    longitude: float
    latitude: float


class DistributionItem(BaseModel):
    name: str
    value: int


class SkillKeyword(BaseModel):
    skill: str
    frequency: int
    heatIndex: float
    category: str
    trendScore: float


class DashboardAnalysis(BaseModel):
    salaryRanges: list[DistributionItem]
    education: list[DistributionItem]
    experience: list[DistributionItem]
    skills: list[SkillKeyword]


class JobLiveItem(BaseModel):
    time: str
    city: str
    title: str
    company: str
    salary: str
    skills: str


class SalaryPredictionRequest(BaseModel):
    city: str = Field(min_length=1)
    industry: str = Field(min_length=1)
    education: str = Field(min_length=1)
    experience: str = Field(min_length=1)
    companySize: str = ""
    jobCategory: str = Field(min_length=1)
    skills: str = ""


class SalaryPrediction(BaseModel):
    predictedMin: float
    predictedMax: float
    predictedAvg: float
    confidence: float
    modelName: str
    explanation: str
    influenceFactors: list[str]


class CareerRecommendationRequest(BaseModel):
    major: str = Field(min_length=1)
    education: str = Field(min_length=1)
    skills: list[str] = Field(default_factory=list)
    expectedCities: list[str] = Field(default_factory=list)
    expectedIndustries: list[str] = Field(default_factory=list)
    expectedSalary: int | None = None


class CareerRecommendation(BaseModel):
    direction: str
    city: str
    industry: str
    jobCategory: str
    matchScore: float
    salaryPotential: int
    reason: str
    skillGaps: list[str]
    suggestions: list[str]
