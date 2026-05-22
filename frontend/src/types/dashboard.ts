export interface RankItem {
  name: string
  value: number
  score: number
  tag: string
}

export interface TrendPoint {
  month: string
  jobs: number
  freshJobs: number
  aiJobs: number
}

export interface DashboardOverview {
  totalJobs: number
  averageSalary: number
  coveredCities: number
  mappableCities: number
  salarySampleRows: number
  coveredRegions: number
  totalRegions: number
  publishStart: string
  publishEnd: string
  freshFriendlyIndex: number
  hotCities: RankItem[]
  hotIndustries: RankItem[]
  monthlyTrend: TrendPoint[]
}

export interface ProvinceMetric {
  province: string
  jobCount: number
  avgSalary: number
  freshFriendlyIndex: number
  heatIndex: number
  topIndustry: string
  growthRate: number
}

export interface CityMetric {
  province: string
  city: string
  jobCount: number
  avgSalary: number
  freshFriendlyIndex: number
  attractionIndex: number
  rankNo: number
  hasCoords: boolean
  longitude: number
  latitude: number
}

export interface DistributionItem {
  name: string
  value: number
}

export interface SkillKeyword {
  skill: string
  frequency: number
  heatIndex: number
  category: string
  trendScore: number
}

export interface DashboardAnalysis {
  salaryRanges: DistributionItem[]
  education: DistributionItem[]
  experience: DistributionItem[]
  skills: SkillKeyword[]
}

export interface JobLiveItem {
  time: string
  city: string
  title: string
  company: string
  salary: string
  skills: string
}

export interface SalaryPredictionRequest {
  city: string
  industry: string
  education: string
  experience: string
  companySize: string
  jobCategory: string
  skills: string
}

export interface SalaryPrediction {
  predictedMin: number
  predictedMax: number
  predictedAvg: number
  confidence: number
  modelName: string
  explanation: string
  influenceFactors: string[]
}

export interface CareerRecommendationRequest {
  major: string
  education: string
  skills: string[]
  expectedCities: string[]
  expectedIndustries: string[]
  expectedSalary: number
}

export interface CareerRecommendation {
  direction: string
  city: string
  industry: string
  jobCategory: string
  matchScore: number
  salaryPotential: number
  reason: string
  skillGaps: string[]
  suggestions: string[]
}

export interface AdminSession {
  token: string
  username: string
  expiresAt: string
}

export interface AdminAuditRecord {
  id: string
  username: string
  loginTime: string
  reportedIp: string
  observedIp: string
  userAgent: string
  source: string
  status: string
  note: string
}

export interface AdminDeleteAuditResult {
  deletedId: string
  backupFile: string
}

export interface AdminDeleteSecurityError {
  remainingAttempts: number
  maxAttempts: number
  banned: boolean
  blockedUntil: string
}

export interface AdminBannedIpRecord {
  ip: string
  attempts: number
  blockedUntil: string
}

export interface AdminUnbanIpResult {
  ip: string
  unbanned: boolean
}
