# Python 后端接口

本目录使用 FastAPI 实现就业态势感知平台后端，不使用 Java。

## 启动

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

接口根路径：`http://localhost:8000/api`

## 核心接口

- `GET /api/dashboard/overview`
- `GET /api/dashboard/provinces`
- `GET /api/dashboard/cities/ranking`
- `GET /api/dashboard/analysis`
- `GET /api/dashboard/skills`
- `GET /api/dashboard/live-jobs`
- `POST /api/predict/salary`
- `POST /api/recommend/career`

当前服务默认返回演示聚合数据，便于答辩展示。接入 MySQL 时，可在 `app/core/config.py` 中配置数据库连接，并将 `app/services/demo_data.py` 替换为 SQLAlchemy 查询。
