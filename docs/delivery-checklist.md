# 交付与验证清单

## 项目目标

实现《面向高校毕业生的中国就业态势感知与职业决策支持平台》，体现“大数据分析 + 智能预测 + 职业推荐 + 动态可视化大屏 + 决策支持”，并按用户要求使用 Python 后端，不使用 Java 后端。

## 交付物

- 设计文档：`docs/project-design.md`
- 大屏预览截图：`docs/dashboard-preview.png`
- Python FastAPI 后端：`backend/`
- Vue3 + TypeScript + ECharts 多模块前端平台：`frontend/`
- OpenRouter AI 推荐配置示例：`.env.example`、`backend/.env.example`
- 真实中国地图 GeoJSON：`frontend/src/assets/china.geo.json`
- MySQL 数据库 SQL：`database/schema.sql`、`database/seed.sql`
- 数据处理与模型训练：`data-processing/pipeline.py`
- 样例数据与输出：`data-processing/sample_jobs.csv`、`data-processing/output/`

## Prompt-to-Artifact 对照

| 要求 | 证据 |
|---|---|
| 项目背景与研究意义 | `docs/project-design.md` 第 1 节 |
| 系统需求分析 | `docs/project-design.md` 第 2 节 |
| 系统功能模块设计 | `docs/project-design.md` 第 3 节 |
| 数据库表结构设计 | `docs/project-design.md` 第 4 节，`database/schema.sql` |
| 数据处理流程 | `docs/project-design.md` 第 5 节，`data-processing/pipeline.py` |
| 核心算法设计 | `docs/project-design.md` 第 6 节，`data-processing/pipeline.py`，`backend/app/services/` |
| 动态可视化大屏设计方案 | `docs/project-design.md` 第 7 节，`frontend/src/App.vue` |
| 前后端系统架构设计 | `docs/project-design.md` 第 8 节 |
| 毕业论文目录结构 | `docs/project-design.md` 第 9 节 |
| 创新点与可行性分析 | `docs/project-design.md` 第 10 节 |
| 大屏页面布局草图说明 | `docs/project-design.md` 第 11 节 |
| 大屏动态效果实现方案 | `docs/project-design.md` 第 12 节 |
| Python 后端接口 | `backend/app/main.py`，`backend/app/routers/` |
| 薪资预测接口 | `POST /api/predict/salary`，`backend/app/services/prediction.py` |
| 职业推荐接口 | `POST /api/recommend/career`，`backend/app/services/recommendation.py` |
| OpenRouter AI 接入 | `backend/app/services/ai_client.py`，`backend/app/core/config.py`，`docker-compose.yml` |
| AI 不可用兜底 | `backend/app/services/prediction.py`，`backend/app/services/recommendation.py` |
| 登录默认入口 | `frontend/src/App.vue`，默认 `isAuthenticated = false` |
| 管理员登录审计与 IP 封禁 | `backend/app/routers/admin.py`，`backend/app/services/audit_log.py`，`frontend/src/App.vue` |
| 管理员删除/解除封禁密码哈希 | `backend/app/core/passwords.py`，`backend/app/core/config.py` |
| ECharts 中国地图、飞线、涟漪、轮播高亮 | `frontend/src/components/ChinaMap.vue`，`frontend/src/assets/china.geo.json` |
| 数字翻牌 | `frontend/src/components/MetricCard.vue`，`frontend/src/composables/useAnimatedNumber.ts` |
| 排行榜自动滚动 | `frontend/src/components/AutoRank.vue` |
| 实时岗位持续滚动 | `frontend/src/components/LiveJobTicker.vue` |
| 趋势图时间窗播放 | `frontend/src/components/TrendChart.vue` |
| 技能词云/标签流动 | `frontend/src/components/SkillCloud.vue` |
| 1920x1080 大屏布局 | `frontend/src/App.vue`，`frontend/src/styles/base.css` |
| 多页面业务功能 | `frontend/src/App.vue` 顶部模块导航与 workbench 页面 |
| 全国省级数据覆盖 | `frontend/src/services/mockData.ts`，`backend/app/services/demo_data.py`，`database/seed.sql` |
| 城市评估页面 | `frontend/src/App.vue` 城市卡片与省份覆盖表 |
| 薪资预测页面 | `frontend/src/App.vue`，`frontend/src/components/DecisionPanel.vue` |
| 技能挖掘页面 | `frontend/src/App.vue`，`frontend/src/components/SkillCloud.vue` |
| 职业推荐页面 | `frontend/src/App.vue`，`frontend/src/components/DecisionPanel.vue` |
| 数据治理页面 | `frontend/src/App.vue` 数据流水线与覆盖说明 |

## 验证结果

已执行并通过：

```bash
cd frontend
npm run build
```

```bash
python -m pytest backend\tests
```

```bash
python -m compileall backend data-processing
```

```bash
python data-processing\pipeline.py --input data-processing\sample_jobs.csv --output data-processing\output
```

运行态验证：

- `GET http://127.0.0.1:8000/api/health` 返回 `runtime = python-fastapi`
- `GET http://127.0.0.1:8000/api/dashboard/overview` 返回 `code = 200`
- `GET http://127.0.0.1:8000/api/dashboard/skills` 返回技能热度数据
- `POST http://127.0.0.1:8000/api/recommend/career` 返回 3 条职业推荐；AI 账户不可用时自动使用本地规则兜底
- `GET http://127.0.0.1:5173` 返回 `200`
- 浏览器刷新首页默认进入登录页，点击“进入平台”后进入系统，点击“退出登录”后回到登录页
- 浏览器控制台无业务错误

## 当前本地服务

- 前端平台：`http://127.0.0.1:5173`
- Python 后端：`http://127.0.0.1:8000/api`

## 说明

前端支持后端接口不可用时回退到由真实快照生成的兜底数据；当前已验证前端能通过 Vite 代理调用 Python FastAPI 接口。当前真实快照覆盖 37772 条岗位记录，大陆 31 个省级区域均有样本，澳门和台湾显示“样本不足”，不使用虚构岗位数、薪资或热度补齐。

`v4.0.0` 的 AI 能力和管理员安全能力都通过后端环境变量启用。真实密钥、`ADMIN_SECURITY_PEPPER`、`ADMIN_DELETE_PASSWORD_HASH`、`ADMIN_UNBAN_PASSWORD_HASH` 只放在本地 `backend/.env` 或部署用根目录 `.env`，不要提交到 Git。OpenRouter 返回额度不足、限流或模型不可用时，职业推荐和薪资解释接口会保留本地规则结果。

数据处理测试样例 `sample_jobs.csv` 只有 10 条记录，仅用于验证脚本能运行；真实论文实验应使用 `data-processing/data/project_jobs_real.csv` 和 `data-processing/output/` 下的最新输出。如果真实数据中某省岗位样本不足，应在页面和论文中标注“样本不足/置信度较低”，不应直接留空。
