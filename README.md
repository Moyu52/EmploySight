# 面向高校毕业生的中国就业态势感知与职业决策支持平台

本项目是一个面向高校毕业生、就业指导老师和高校就业管理部门的智能化就业决策支持平台。系统提供“就业态势感知 + 城市评估 + 薪资预测 + 技能挖掘 + AI 职业推荐 + 数据治理”的完整毕业设计实现，后端使用 Python FastAPI，不使用 Java。当前大屏数据已由 Kaggle 与中国公共招聘网真实岗位快照生成，真实数据来源、官网地址和校验方法见 `docs/data-source-verification.md`。

当前版本：`v3.0.3`。本版本接入 ZenMux/Gemini 生成职业路径建议和薪资解释，补齐登录页默认入口，并保留本地规则兜底，避免 AI 服务不可用时影响平台访问。

## 项目结构

```text
.
├─ backend/                 Python FastAPI 后端接口
├─ frontend/                Vue3 + TypeScript + ECharts 平台前端
├─ database/                MySQL 建表 SQL 与全国省市初始化样例数据
├─ data-processing/         Pandas / Scikit-learn / jieba 数据处理与模型脚本
└─ docs/                    毕业设计方案、交付清单、预览截图
```

## 功能模块

- 态势大屏：全国就业热度地图、核心指标、城市排行、行业排行、薪资学历经验分布、技能热度、实时岗位流。
- 城市评估：城市就业吸引力卡片、省份就业热度表、岗位规模、平均薪资、应届友好度和行业结构。
- 登录入口：默认先进入平台访问页，选择账号、密码和角色后进入系统，退出后回到登录页。
- 薪资预测：基于城市、行业、学历、经验、公司规模、岗位类别和技能标签预测岗位薪资区间，并在配置 AI 后生成解释。
- 技能挖掘：对岗位标题和描述进行中文分词、TF-IDF、TextRank 与技能词统计，形成技能热度排行。
- 职业推荐：按专业、学历、技能、期望城市和行业输出岗位方向、目标城市和技能提升建议；配置 ZenMux 后由 Gemini 生成更完整的推荐理由和行动建议。
- 数据治理：展示 Kaggle CSV 到指标库、模型和接口的处理流程，说明数据覆盖和样本置信度口径。

## 数据覆盖

当前真实数据快照为 `data-processing/data/project_jobs_real.csv`，合并了 Kaggle `China Jobs Data`、Kaggle `Job Posting Data in China` 和中国公共招聘网公开岗位列表，共 37772 条岗位记录，其中 37380 条有效薪资样本进入薪资分析和模型训练。中国公共招聘网样本发布时间范围为 2025-05-27 至 2026-05-19，近一年岗位占主体。

大陆 31 个省级区域均有真实岗位样本，香港有 Kaggle 样本；澳门、台湾暂无同口径岗位样本，系统显示“样本不足”，不使用虚构岗位数、薪资或热度补齐。

数据真实性说明、官网地址、字段对应关系和校验方法见：`docs/data-source-verification.md`。

服务器迁移、Nginx 配置、后端启动和真实数据接入流程见：`docs/server-migration-and-data-integration.md`。

Docker 容器化部署、软件检测、Compose 启动、MySQL 容器和容器内数据刷新流程见：`docs/docker-deployment.md`。

## 快速启动

### 前端平台

```bash
cd frontend
npm install
npm run dev
```

默认地址：`http://localhost:5173`

### Python 后端接口

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

默认地址：`http://localhost:8000/api`

AI 职业推荐与薪资解释需要在 `backend/.env` 中配置 ZenMux：

```env
ZENMUX_API_KEY=你的 ZenMux API Key
ZENMUX_BASE_URL=https://zenmux.ai/api/v1
ZENMUX_MODEL=google/gemini-3.5-flash-free
AI_ENABLED=true
```

Docker Compose 部署时，把同样的 `ZENMUX_API_KEY` 填到项目根目录 `.env`。未配置密钥时系统会继续使用本地规则推荐。

如果 ZenMux 返回余额不足、限流或模型不可用，后端接口仍会返回本地规则结果，前端页面不会中断。

### 数据库

先创建 MySQL 数据库，再执行：

```sql
source database/schema.sql;
source database/seed.sql;
```

### 数据处理

```bash
cd data-processing
pip install -r requirements.txt
python prepare_kaggle_data.py
python collect_mohrss_jobs.py --pages-per-province 80 --workers 8
python build_project_dataset.py
python pipeline.py --input data/project_jobs_real.csv --output output
python export_dashboard_data.py
```

## 验证

```bash
cd frontend
npm run build
```

```bash
python -m pytest backend\tests
python -m compileall backend data-processing
python data-processing\pipeline.py --input data-processing\sample_jobs.csv --output data-processing\output
```
