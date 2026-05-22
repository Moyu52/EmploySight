from fastapi import APIRouter

from app.schemas import ApiResponse, CareerRecommendationRequest
from app.services.recommendation import recommend_career_with_ai

router = APIRouter()


@router.post("/career", response_model=ApiResponse)
def career(payload: CareerRecommendationRequest) -> ApiResponse:
    return ApiResponse(data=recommend_career_with_ai(payload))
