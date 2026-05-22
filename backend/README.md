# Python 后端接口

本目录使用 FastAPI 实现就业态势感知平台后端，不使用 Java。当前版本为 `v3.0.3`，职业推荐和薪资解释支持通过 ZenMux 调用 Gemini，未配置或调用失败时自动回退本地规则。

## 启动

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

接口根路径：`http://localhost:8000/api`

## AI 配置

职业推荐和薪资预测解释支持通过 ZenMux 调用 Gemini。复制 `backend/.env.example` 为 `backend/.env`，填写：

```env
ZENMUX_API_KEY=你的 ZenMux API Key
ZENMUX_BASE_URL=https://zenmux.ai/api/v1
ZENMUX_MODEL=google/gemini-3.5-flash-free
AI_ENABLED=true
```

未填写 `ZENMUX_API_KEY` 或调用失败时，接口会自动使用本地规则兜底。

常见调用失败场景包括 ZenMux 账户余额不足、模型不可用、网络超时或 SDK 未安装。生产部署时不要把密钥写到前端，只放在后端 `.env` 或 Docker Compose 环境变量中。

## 核心接口

- `GET /api/dashboard/overview`
- `GET /api/dashboard/provinces`
- `GET /api/dashboard/cities/ranking`
- `GET /api/dashboard/analysis`
- `GET /api/dashboard/skills`
- `GET /api/dashboard/live-jobs`
- `POST /api/predict/salary`
- `POST /api/recommend/career`

`POST /api/recommend/career` 会先生成本地基线推荐，再尝试让 AI 根据学生画像和基线结果生成更完整的方向、理由、技能差距和行动建议。

`POST /api/predict/salary` 保留本地薪资数值模型，只让 AI 生成解释和影响因素，避免 AI 随意改动薪资区间。

当前服务默认返回由 `data-processing/data/project_jobs_real.csv` 生成的真实聚合快照。接入 MySQL 时，可在 `app/core/config.py` 中配置数据库连接，并将 `app/services/demo_data.py` 替换为 SQLAlchemy 查询。
