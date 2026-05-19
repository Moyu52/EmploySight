import type {
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

export function fetchOverview() {
  return request<DashboardOverview>('/api/dashboard/overview', overview)
}

export function fetchProvinces() {
  return request<ProvinceMetric[]>('/api/dashboard/provinces', provinceMetrics)
}

export function fetchCities() {
  return request<CityMetric[]>('/api/dashboard/cities/ranking', cityMetrics)
}

export function fetchAnalysis() {
  return request<DashboardAnalysis>('/api/dashboard/analysis', analysis)
}

export function fetchLiveJobs() {
  return request<JobLiveItem[]>('/api/dashboard/live-jobs', liveJobs)
}

export function predictSalary(payload: SalaryPredictionRequest) {
  return request<SalaryPrediction>('/api/predict/salary', mockSalaryPrediction, {
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
