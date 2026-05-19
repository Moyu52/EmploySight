# 数据来源与真实性说明

本文档用于说明本项目使用或计划接入的数据来源、官网地址、字段用途、验证方法和当前数据真实性状态。

结论先写清楚：2026-05-19 已下载 Kaggle `China Jobs Data`、Kaggle `Job Posting Data in China`，并补充采集中国公共招聘网公开岗位列表，合并生成 `data-processing/data/project_jobs_real.csv`。当前前后端大屏数据已由该真实数据快照生成；`data-processing/sample_jobs.csv` 仍然只是 pipeline 测试样例，`database/seed.sql` 仍然只是数据库初始化样例。

当前真实快照覆盖 37772 条岗位记录，其中 37380 条进入薪资模型和薪资分布分析；大陆 31 个省级区域均有真实岗位样本，香港有少量 Kaggle 样本，澳门和台湾暂无同口径岗位样本，页面应显示“样本不足”，不能用虚构数值补齐。中国公共招聘网样本发布时间范围为 2025-05-27 至 2026-05-19，近一年岗位占主体。

## 1. 当前项目内数据状态

| 文件/模块 | 当前用途 | 是否真实原始数据 | 处理要求 |
| --- | --- | --- | --- |
| `frontend/src/services/mockData.ts` | 前端接口失败时的兜底展示数据 | 是，已由真实快照生成 | 文件名保留为接口兜底兼容，内容来自 `project_jobs_real.csv` |
| `backend/app/services/demo_data.py` | FastAPI 后端大屏接口数据 | 是，已由真实快照生成 | 文件名保留为接口兼容，内容来自 `project_jobs_real.csv` |
| `database/seed.sql` | MySQL 初始化样例数据 | 否 | 只能用于建表和演示导入流程 |
| `data-processing/sample_jobs.csv` | 数据处理脚本测试样例 | 否 | 只用于验证 pipeline 能运行 |
| `data-processing/raw/kaggle_china_jobs_data.zip` | Kaggle 原始下载包 | 是 | `China Jobs Data` 原始压缩包 |
| `data-processing/raw/kaggle_job_posting_data_in_china.zip` | Kaggle 原始下载包 | 是 | `Job Posting Data in China` 原始压缩包 |
| `data-processing/data/mohrss_public_jobs.csv` | 中国公共招聘网公开岗位采集结果 | 是 | 用于补足大陆省级覆盖 |
| `data-processing/data/project_jobs_real.csv` | 项目真实岗位合并数据 | 是 | 当前前后端与 pipeline 的主数据输入 |
| `frontend/src/assets/china.geo.json` | 中国地图边界 GeoJSON | 是地图可视化底图数据，但非招聘数据 | 需要在论文中单独说明地图来源 |
| `data-processing/pipeline.py` | 真实 CSV 清洗、聚合和建模脚本 | 脚本本身不含数据 | 应使用真实 CSV 重新运行 |

## 2. 真实数据来源清单

### 2.1 招聘岗位明细数据

| 数据源 | 官网地址 | 数据性质 | 可用于项目中的字段 |
| --- | --- | --- | --- |
| Kaggle - China Jobs Data | https://www.kaggle.com/datasets/polartech/china-jobs-data | 中国招聘岗位数据集，Kaggle 页面说明包含数百万条中国岗位数据 | 岗位名称、公司、城市/地区、薪资、发布日期、经验、学历、行业、专业、公司规模、经纬度 |
| Kaggle - Job Posting Data in China | https://www.kaggle.com/datasets/techsalerator/job-posting-data-in-china/versions/1 | 中国岗位发布数据集 | 岗位名称、公司、地区、岗位描述、薪资、行业、招聘要求 |
| 中国公共招聘网 | https://job.mohrss.gov.cn/ | 人力资源和社会保障部相关公共招聘平台 | 岗位名称、单位名称、地区、岗位类别、招聘人数、学历、经验、薪资等页面公开字段 |
| 中国公共招聘网 - 招聘岗位页 | https://job.mohrss.gov.cn/cjobs/jobinfolist/listJobinfolistIndex | 岗位检索入口 | 可用于人工抽样核验岗位是否存在 |

说明：Kaggle 是公开数据集平台，不等同于政府官网。若论文要求“官方数据”，建议以中国公共招聘网、国家大学生就业服务平台等官方平台为主；若使用 Kaggle，应在论文中写成“公开数据集”，不能写成政府官方统计数据。

## 2.1.1 当前真实快照记录

| 项目 | 记录 |
| --- | --- |
| 生成时间 | 2026-05-19 18:44:21 +08:00 |
| 合并文件 | `data-processing/data/project_jobs_real.csv` |
| 合并文件 SHA256 | `5863A680538482C7AA9A851B08B397B301EC40A9ED42980E479F8E143864D45E` |
| 总岗位记录 | 37772 |
| 有薪资记录 | 37389，pipeline 清洗后有效薪资样本 37380 |
| 数据源构成 | Kaggle China Jobs Data 999 条；Kaggle Job Posting Data in China 中国岗位 375 条；中国公共招聘网 36398 条 |
| 最新公共招聘数据时间范围 | 2025-05-27 至 2026-05-19，其中 2026 年岗位 33549 条 |
| 区域覆盖 | 大陆 31 个省级区域均有样本；香港 5 条；澳门、台湾暂无同口径岗位样本 |
| 模型训练指标 | MAE 1560.88；RMSE 2678.21；R2 0.4431 |
| 隐私处理 | 中国公共招聘网页面中的联系人、电话等字段未导出到项目数据 |

### 2.2 工资、行业和就业统计校验数据

| 数据源 | 官网地址 | 数据性质 | 项目用途 |
| --- | --- | --- | --- |
| 国家统计局 - 国家数据 | https://data.stats.gov.cn/ | 国家统计数据库 | 用于校验就业人员、行业、地区、工资等宏观指标 |
| 国家统计局 - 2024 年城镇单位就业人员年平均工资情况 | https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202505/t20250516_1959826.html | 官方工资统计发布 | 校验薪资分布、行业薪资差异和地区薪资基准 |
| 人力资源和社会保障部 | https://www.mohrss.gov.cn/ | 就业、人社政策与统计信息发布部门 | 用于就业政策、公共招聘平台说明、就业服务口径 |

国家统计局 2024 年工资数据可作为宏观校验来源，例如行业平均工资、区域平均工资和规模以上企业岗位类别工资。项目中的岗位薪资来自招聘岗位，口径和统计局平均工资不同，不能直接说二者完全一致，只能用于合理性校验。

### 2.3 高校毕业生就业场景数据

| 数据源 | 官网地址 | 数据性质 | 项目用途 |
| --- | --- | --- | --- |
| 国家大学生就业服务平台 | https://www.ncss.cn/ | 高校毕业生就业服务平台 | 用于高校毕业生就业服务、校园招聘、岗位信息核验 |
| 教育部 | https://www.moe.gov.cn/ | 高校毕业生就业政策、规模和公告 | 用于论文背景中的毕业生就业规模、政策依据 |

这些数据适合用于“毕业生就业背景”和“政策环境”说明，不应直接替代招聘岗位明细数据。

### 2.4 地图边界数据

| 数据源 | 官网地址 | 数据性质 | 项目用途 |
| --- | --- | --- | --- |
| GeoJSON.CN 中国地图数据集 | https://geojson.cn/data/atlas/china | 中国省市县 GeoJSON/TopoJSON 地图数据 | 当前项目 `china.geo.json` 的地图边界来源 |
| 国家地理信息公共服务平台 天地图 | https://www.zhmap.gov.cn/ | 国家级地理信息公共服务平台 | 严格地图合规场景建议优先核验 |
| 自然资源部标准地图服务系统 | http://bzdt.ch.mnr.gov.cn/index.html | 标准地图服务 | 论文或公开展示时用于核验中国地图边界合规性 |

地图数据只用于可视化边界，不代表就业数据来源。

## 3. 项目指标与真实数据的对应关系

| 项目指标 | 数据来源字段 | 生成方式 | 是否应直接来自官网 |
| --- | --- | --- | --- |
| 全国岗位总数 | 岗位明细表 `job_title` / `job_id` | 按清洗后的岗位记录计数 | 否，来自岗位数据聚合 |
| 省份就业热度 | 岗位数、平均薪资、增长率、应届友好度 | `pipeline.py` 聚合并加权计算 | 否，是模型指标 |
| 城市吸引力指数 | 城市岗位数、平均薪资、行业多样性、应届友好度 | `pipeline.py` 聚合并加权计算 | 否，是模型指标 |
| 平均月薪 | 招聘薪资字段 | 解析薪资区间后取均值 | 否，来自岗位明细 |
| 学历要求分布 | `degreeString` / 学历字段 | 标准化后分组统计 | 否，来自岗位明细 |
| 经验要求分布 | `workYearString` / 经验字段 | 标准化后分组统计 | 否，来自岗位明细 |
| 技能需求热度 | 岗位名称、岗位描述、技能字段 | 分词、词频、TF-IDF、TextRank、热度归一化 | 否，是文本挖掘结果 |
| 近 12 个月岗位趋势 | 发布日期、岗位数量 | 按月份聚合岗位数量 | 否，来自岗位明细 |
| 薪资预测模型 | 城市、行业、学历、经验、公司规模、岗位类别、技能、薪资 | 训练随机森林回归模型 | 否，是机器学习结果 |

## 4. 真实数据替换流程

1. 从真实来源下载 CSV 或导出岗位明细。
2. 将文件放入 `data-processing/data/`，例如：

```powershell
mkdir data-processing\data
```

3. 使用数据处理脚本重新生成清洗结果：

```powershell
cd data-processing
python pipeline.py --input data/jobs.csv --output output
```

4. 检查输出文件：

| 输出文件 | 用途 |
| --- | --- |
| `output/clean_jobs.csv` | 清洗后的真实岗位明细 |
| `output/province_index.csv` | 省份就业热度指标 |
| `output/city_index.csv` | 城市就业吸引力指标 |
| `output/skill_keywords.csv` | 技能关键词热度 |
| `output/model_metrics.json` | 薪资预测模型评估结果 |
| `output/salary_model.joblib` | 薪资预测模型 |

5. 使用 `export_dashboard_data.py` 将输出指标同步到 FastAPI 聚合快照和前端接口兜底数据。
6. `mockData.ts` 和 `demo_data.py` 文件名保留为接口兼容，内容已由真实快照生成；`sample_jobs.csv` 和 `seed.sql` 仍只作为测试/初始化样例。

## 5. 数据真实性校验方法

### 5.1 文件级校验

真实数据下载后，应记录：

| 项目 | 记录内容 |
| --- | --- |
| 下载日期 | 例如 `2026-05-19` |
| 下载地址 | 数据集官网 URL |
| 原始文件名 | Kaggle 或官网导出的 CSV 文件名 |
| 原始记录数 | CSV 行数 |
| 字段列表 | CSV 表头 |
| 文件哈希 | `Get-FileHash 文件名 -Algorithm SHA256` |

PowerShell 示例：

```powershell
Get-FileHash data-processing\data\jobs.csv -Algorithm SHA256
```

### 5.2 记录级抽样核验

至少抽样 20 条岗位记录，回到官网或平台页面核验：

| 核验项 | 要求 |
| --- | --- |
| 岗位名称 | 与官网岗位一致 |
| 公司名称 | 与官网岗位一致 |
| 城市/地区 | 与官网岗位一致 |
| 薪资 | 与官网公开薪资一致或说明缺失 |
| 学历/经验 | 与官网公开要求一致 |
| 发布时间 | 与官网公开时间一致 |

### 5.3 统计级合理性校验

将项目聚合结果与国家统计局数据做口径说明：

- 项目薪资是招聘岗位薪资，不等于国家统计局就业人员实际工资。
- 项目岗位数是招聘发布量，不等于真实就业人数。
- 项目行业热度是招聘需求热度，不等于行业总产值或就业存量。
- 省份或城市样本过少时，页面和论文应标注“样本不足/置信度较低”。

## 6. 论文和答辩中建议写法

可以写：

> 本项目岗位明细数据来源于公开招聘岗位数据集和公共招聘平台。项目首先对原始岗位数据进行字段统一、薪资解析、学历经验标准化和城市省份标准化，再按省份、城市、行业、学历、经验、技能等维度进行聚合分析。国家统计局数据用于宏观工资和就业统计口径校验，地图边界数据用于可视化展示。

不能写：

> 本项目当前前端 mock 数据、后端 demo 数据和 seed.sql 中的数值全部来源于真实官网。

因为 `seed.sql` 和 `sample_jobs.csv` 只是测试/初始化样例；前端 `mockData.ts` 与后端 `demo_data.py` 虽然文件名保留为兼容旧接口，但内容已由真实快照生成，应在论文中单独说明。

## 7. 当前已完成的真实数据整改

当前项目已经完成以下真实数据整改：

1. 下载 Kaggle 原始压缩包，并保存 Kaggle 页面 HTML 与元数据。
2. 采集中国公共招聘网公开岗位列表，保存采集 CSV、采集时间、记录数和 SHA256。
3. 使用 `data-processing/pipeline.py` 重新生成清洗数据、聚合指标、技能关键词和薪资模型。
4. 使用 `data-processing/export_dashboard_data.py` 重新生成前端兜底数据和后端聚合快照。
5. 页面中澳门、台湾显示“样本不足”，不使用虚构岗位数、薪资或热度补齐。
6. 保留 `data-processing/sample_jobs.csv` 与 `database/seed.sql` 为测试/初始化样例，不作为真实分析数据。
