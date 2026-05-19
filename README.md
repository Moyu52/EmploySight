# 面向高校毕业生的中国就业态势感知与职业决策支持平台

本项目是一个面向高校毕业生、就业指导老师和高校就业管理部门的智能化就业决策支持平台。系统提供“就业态势感知 + 城市评估 + 薪资预测 + 技能挖掘 + 职业推荐 + 数据治理”的完整毕业设计实现，后端使用 Python FastAPI，不使用 Java。当前仓库内置数据主要用于原型演示，真实数据来源、官网地址和替换要求见 `docs/data-source-verification.md`。

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
- 薪资预测：基于城市、行业、学历、经验、公司规模、岗位类别和技能标签预测岗位薪资区间。
- 技能挖掘：对岗位标题和描述进行中文分词、TF-IDF、TextRank 与技能词统计，形成技能热度排行。
- 职业推荐：按专业、学历、技能、期望城市和行业输出岗位方向、目标城市和技能提升建议。
- 数据治理：展示 Kaggle CSV 到指标库、模型和接口的处理流程，说明数据覆盖和样本置信度口径。

## 数据覆盖

前端演示数据、Python 后端演示接口和 MySQL 初始化样例均已覆盖 34 个省级行政区，并补充 38 个重点城市/省会城市指标，避免地图和省份表出现大量空白。

演示数据只能用于答辩原型展示，不能作为真实统计结论或论文实验数据。正式论文实验应将真实岗位 CSV 放入 `data-processing/data/`，通过 `data-processing/pipeline.py` 重新清洗、聚合、训练并导入 MySQL。若真实数据中某个省份样本不足，系统应标注“样本不足/置信度较低”，不应直接留空。

数据真实性说明、官网地址、字段对应关系和校验方法见：`docs/data-source-verification.md`。

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
python pipeline.py --input data/jobs.csv --output output
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
