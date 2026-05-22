# Python 后端接口

本目录使用 FastAPI 实现就业态势感知平台后端，不使用 Java。当前版本为 `v4.0.0`，职业推荐和薪资解释支持通过 OpenRouter 调用 OpenAI-compatible Chat Completions，未配置或调用失败时自动回退本地规则。管理员侧提供登录审计、删除密码防爆破、临时封禁 IP 和解除封禁能力。

## 启动

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

接口根路径：`http://localhost:8000/api`

## AI 配置

职业推荐和薪资预测解释支持通过 OpenRouter。复制 `backend/.env.example` 为 `backend/.env`，填写：

```env
AI_ENABLED=true
AI_API_KEY=你的 OpenRouter API Key
AI_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=openai/gpt-oss-120b:free
OPENROUTER_APP_NAME=EmploySight
```

未填写 `AI_API_KEY` 或调用失败时，接口会自动使用本地规则兜底。

常见调用失败场景包括 OpenRouter 额度不足、模型不可用、网络超时或 SDK 未安装。生产部署时不要把密钥写到前端，只放在后端 `.env` 或 Docker Compose 环境变量中。

## 管理员与登录审计

管理员账号通过后端 `.env` 配置，默认示例为：

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_SECURITY_PEPPER=生成的随机 pepper
ADMIN_DELETE_PASSWORD_HASH=pbkdf2_sha256$v1$...
ADMIN_UNBAN_PASSWORD_HASH=pbkdf2_sha256$v1$...
ADMIN_DELETE_MAX_ATTEMPTS=3
ADMIN_DELETE_BAN_MINUTES=30
AUDIT_LOG_PATH=data/admin_login_audit.jsonl
AUDIT_BACKUP_DIR=data/admin_login_backups
```

审计记录会保存登录时间、用户名、请求头上报 IP 和后端记录 IP。请求头上报 IP 可能被伪造；后端记录 IP 仍会受可信代理配置影响，用户使用 VPN 或代理时通常是 VPN/代理出口地址。

删除审计记录需要输入删除密码，后端只保存 `ADMIN_DELETE_PASSWORD_HASH`，不保存明文。删除密码连续错误达到 `ADMIN_DELETE_MAX_ATTEMPTS` 次后，当前请求 IP 会被临时封禁 `ADMIN_DELETE_BAN_MINUTES` 分钟，防止暴力破解删除密码。

解除封禁 IP 需要输入独立的解除封禁密码，后端只保存 `ADMIN_UNBAN_PASSWORD_HASH`。当前示例哈希使用 PBKDF2-HMAC-SHA256、独立 salt、用途前缀和 `ADMIN_SECURITY_PEPPER` 进行校验；部署时建议重新生成 pepper 和哈希。

## 核心接口

- `GET /api/dashboard/overview`
- `GET /api/dashboard/provinces`
- `GET /api/dashboard/cities/ranking`
- `GET /api/dashboard/analysis`
- `GET /api/dashboard/skills`
- `GET /api/dashboard/live-jobs`
- `POST /api/predict/salary`
- `POST /api/recommend/career`
- `POST /api/admin/login`
- `POST /api/admin/login-events`
- `GET /api/admin/login-events`
- `GET /api/admin/banned-ips`
- `POST /api/admin/unban-ip`
- `DELETE /api/admin/login-events/{record_id}`

`POST /api/recommend/career` 会先生成本地基线推荐，再尝试让 AI 根据学生画像和基线结果生成更完整的方向、理由、技能差距和行动建议。

`POST /api/predict/salary` 保留本地薪资数值模型，只让 AI 生成解释和影响因素，避免 AI 随意改动薪资区间。

当前服务默认返回由 `data-processing/data/project_jobs_real.csv` 生成的真实聚合快照。接入 MySQL 时，可在 `app/core/config.py` 中配置数据库连接，并将 `app/services/demo_data.py` 替换为 SQLAlchemy 查询。
