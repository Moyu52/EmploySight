from typing import Any

from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any


class AdminLoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=200)


class AdminLoginResponse(BaseModel):
    token: str
    username: str
    expiresAt: str


class PlatformLoginEventRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)


class AdminAuditRecord(BaseModel):
    id: str
    username: str
    loginTime: str
    reportedIp: str
    observedIp: str
    userAgent: str
    source: str
    status: str
    note: str


class AdminDeleteAuditRequest(BaseModel):
    deletePassword: str = Field(min_length=1, max_length=200)


class AdminDeleteAuditResponse(BaseModel):
    deletedId: str
    backupFile: str


class AdminDeleteSecurityError(BaseModel):
    remainingAttempts: int
    maxAttempts: int
    banned: bool = False
    blockedUntil: str = ""


class AdminBannedIpRecord(BaseModel):
    ip: str
    attempts: int
    blockedUntil: str


class AdminUnbanIpRequest(BaseModel):
    ip: str = Field(min_length=1, max_length=80)
    unbanPassword: str = Field(min_length=1, max_length=200)


class AdminUnbanIpResponse(BaseModel):
    ip: str
    unbanned: bool


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
    mappableCities: int = 0
    salarySampleRows: int = 0
    coveredRegions: int = 0
    totalRegions: int = 0
    publishStart: str = ""
    publishEnd: str = ""
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
    hasCoords: bool = False
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
