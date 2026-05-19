from app.schemas import SalaryPredictionRequest
from app.services.prediction import predict_salary


def test_predict_salary_returns_valid_range() -> None:
    result = predict_salary(
        SalaryPredictionRequest(
            city="西安",
            industry="生产制造及有关人员",
            education="大专",
            experience="不限",
            companySize="100-499人",
            jobCategory="生产制造与设备操作",
            skills="生产,安全,质量",
        )
    )

    assert result.predictedAvg > 0
    assert result.predictedMax > result.predictedMin
    assert len(result.influenceFactors) >= 5
