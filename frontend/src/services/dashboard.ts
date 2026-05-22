import type {
  AdminAuditRecord,
  AdminBannedIpRecord,
  AdminDeleteAuditResult,
  AdminDeleteSecurityError,
  AdminSession,
  AdminUnbanIpResult,
  CareerRecommendation,
  CareerRecommendationRequest,
  CityMetric,
  DashboardAnalysis,
  DashboardOverview,
  JobLiveItem,
  ProvinceMetric,
  SalaryPrediction,
  SalaryPredictionRequest
} from '../types/dashboard'
import {
  analysis,
  cityMetrics,
  liveJobs,
  mockRecommendations,
  mockSalaryPrediction,
  overview,
  provinceMetrics
} from './mockData'

interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export class ApiRequestError<T = unknown> extends Error {
  status: number
  detail: T | null

  constructor(message: string, status: number, detail: T | null = null) {
    super(message)
    this.name = 'ApiRequestError'
    this.status = status
    this.detail = detail
  }
}

async function request<T>(url: string, fallback: T, options?: RequestInit): Promise<T> {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json'
      },
      ...options
    })
    if (!response.ok) {
      return fallback
    }
    const body = (await response.json()) as ApiResponse<T>
    return body.data ?? fallback
  } catch {
    return fallback
  }
}

async function requestStrict<T>(url: string, options?: RequestInit): Promise<T> {
  const requestOptions = options ?? {}
  const response = await fetch(url, {
    ...requestOptions,
    headers: {
      'Content-Type': 'application/json',
      ...(requestOptions.headers ?? {})
    }
  })
  const body = (await response.json().catch(() => null)) as ApiResponse<T> | null
  if (!response.ok || !body) {
    const rawDetail = body && 'detail' in body ? (body as unknown as { detail?: unknown }).detail : null
    const message = typeof rawDetail === 'object' && rawDetail && 'message' in rawDetail
      ? String((rawDetail as { message?: unknown }).message)
      : body?.message || `Request failed: ${response.status}`
    throw new ApiRequestError(message, response.status, rawDetail ?? null)
  }
  return body.data
}

function isCurrentOverview(data: DashboardOverview) {
  return typeof data.mappableCities === 'number'
    && typeof data.salarySampleRows === 'number'
    && typeof data.coveredRegions === 'number'
    && typeof data.publishStart === 'string'
}

function isCurrentCityMetrics(data: CityMetric[]) {
  return data.length >= cityMetrics.length
    && data.some((item) => item.hasCoords)
    && data.every((item) => typeof item.hasCoords === 'boolean')
}

function fallbackSalaryPrediction(payload: SalaryPredictionRequest): SalaryPrediction {
  const city = cityMetrics.find((item) => item.city === payload.city)
  const base = city?.avgSalary || overview.averageSalary
  const educationFactor = payload.education.includes('博士') ? 1.3
    : payload.education.includes('硕士') ? 1.18
      : payload.education.includes('本科') ? 1.08
        : 1
  const experienceFactor = payload.experience.includes('5年以上') ? 1.28
    : payload.experience.includes('3-5年') ? 1.15
      : payload.experience.includes('1-3年') ? 1.06
        : 1
  const industryFactor = payload.industry.includes('专业技术') ? 1.12
    : payload.industry.includes('机械') || payload.industry.includes('电气') ? 1.08
      : payload.industry.includes('生产制造') ? 1.02
        : payload.industry.includes('服务') ? 0.96
          : 1
  const predictedAvg = Math.round(base * educationFactor * experienceFactor * industryFactor)
  return {
    predictedMin: Math.round(predictedAvg * 0.82),
    predictedMax: Math.round(predictedAvg * 1.24),
    predictedAvg,
    confidence: 72.5,
    modelName: 'SalaryReference',
    explanation: '基于当前城市样本平均薪资生成的区间参考。',
    influenceFactors: [`城市薪资基准：${payload.city}`, `行业结构：${payload.industry}`, `学历门槛：${payload.education}`, `经验要求：${payload.experience}`]
  }
}

export function fetchOverview() {
  return request<DashboardOverview>('/api/dashboard/overview', overview).then((data) => {
    return isCurrentOverview(data) ? data : overview
  })
}

export function fetchProvinces() {
  return request<ProvinceMetric[]>('/api/dashboard/provinces', provinceMetrics)
}

export function fetchCities() {
  return request<CityMetric[]>('/api/dashboard/cities/ranking', cityMetrics).then((data) => {
    return isCurrentCityMetrics(data) ? data : cityMetrics
  })
}

export function fetchAnalysis() {
  return request<DashboardAnalysis>('/api/dashboard/analysis', analysis)
}

export function fetchLiveJobs() {
  return request<JobLiveItem[]>('/api/dashboard/live-jobs', liveJobs)
}

export function predictSalary(payload: SalaryPredictionRequest) {
  return request<SalaryPrediction>('/api/predict/salary', fallbackSalaryPrediction(payload), {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function recommendCareer(payload: CareerRecommendationRequest) {
  return request<CareerRecommendation[]>('/api/recommend/career', mockRecommendations, {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function loginAdmin(username: string, password: string) {
  return requestStrict<AdminSession>('/api/admin/login', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  })
}

export function recordPlatformLogin(username: string) {
  return requestStrict<AdminAuditRecord>('/api/admin/login-events', {
    method: 'POST',
    body: JSON.stringify({ username })
  })
}

export function fetchAdminAuditRecords(token: string, query = '') {
  const params = query.trim() ? `?q=${encodeURIComponent(query.trim())}` : ''
  return requestStrict<AdminAuditRecord[]>(`/api/admin/login-events${params}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}

export function fetchAdminBannedIps(token: string) {
  return requestStrict<AdminBannedIpRecord[]>('/api/admin/banned-ips', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
}

export function deleteAdminAuditRecord(token: string, recordId: string, deletePassword: string) {
  return requestStrict<AdminDeleteAuditResult>(`/api/admin/login-events/${recordId}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ deletePassword })
  })
}

export function unbanAdminIp(token: string, ip: string, unbanPassword: string) {
  return requestStrict<AdminUnbanIpResult>('/api/admin/unban-ip', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ ip, unbanPassword })
  })
}

export function isAdminDeleteSecurityError(value: unknown): value is AdminDeleteSecurityError & { message?: string } {
  return Boolean(value)
    && typeof value === 'object'
    && typeof (value as AdminDeleteSecurityError).remainingAttempts === 'number'
    && typeof (value as AdminDeleteSecurityError).maxAttempts === 'number'
    && typeof (value as AdminDeleteSecurityError).banned === 'boolean'
}
