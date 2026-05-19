from app.schemas import SalaryPredictionRequest
from app.services.prediction import predict_salary


def test_predict_salary_returns_valid_range() -> None:
    result = predict_salary(
        SalaryPredictionRequest(
            city="北京",
            industry="人工智能",
            education="硕士",
            experience="1-3年",
            companySize="100-499人",
            jobCategory="算法工程师",
            skills="Python,机器学习",
        )
    )

    assert result.predictedAvg > 0
    assert result.predictedMax > result.predictedMin
    assert len(result.influenceFactors) >= 5
