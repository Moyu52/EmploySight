from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import dashboard, prediction, recommendation


app = FastAPI(
    title="中国就业态势感知与职业决策支持平台",
    description="面向高校毕业生的就业态势感知、薪资预测与职业推荐 Python API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(prediction.router, prefix="/api/predict", tags=["prediction"])
app.include_router(recommendation.router, prefix="/api/recommend", tags=["recommendation"])


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "runtime": "python-fastapi"}
