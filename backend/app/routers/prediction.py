from fastapi import APIRouter

from app.schemas import ApiResponse, SalaryPredictionRequest
from app.services.prediction import predict_salary_with_ai

router = APIRouter()


@router.post("/salary", response_model=ApiResponse)
def salary(payload: SalaryPredictionRequest) -> ApiResponse:
    return ApiResponse(data=predict_salary_with_ai(payload))
