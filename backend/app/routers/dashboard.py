from fastapi import APIRouter

from app.schemas import ApiResponse
from app.services.demo_data import (
    city_metrics,
    dashboard_analysis,
    dashboard_overview,
    live_jobs,
    province_metrics,
)

router = APIRouter()


@router.get("/overview", response_model=ApiResponse)
def overview() -> ApiResponse:
    return ApiResponse(data=dashboard_overview())


@router.get("/provinces", response_model=ApiResponse)
def provinces() -> ApiResponse:
    return ApiResponse(data=province_metrics())


@router.get("/cities/ranking", response_model=ApiResponse)
def cities() -> ApiResponse:
    return ApiResponse(data=city_metrics())


@router.get("/analysis", response_model=ApiResponse)
def analysis() -> ApiResponse:
    return ApiResponse(data=dashboard_analysis())


@router.get("/skills", response_model=ApiResponse)
def skills() -> ApiResponse:
    return ApiResponse(data=dashboard_analysis().skills)


@router.get("/live-jobs", response_model=ApiResponse)
def live_job_stream() -> ApiResponse:
    return ApiResponse(data=live_jobs())
