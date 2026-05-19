# 数据处理与模型训练

该目录用于处理真实招聘岗位数据：

- `China Jobs Data`
- `Job Posting Data in China`
- 中国公共招聘网公开岗位列表

脚本会完成字段映射、薪资解析、学历经验标准化、城市吸引力指数、应届生友好度、技能关键词热度和薪资预测模型训练。

## 使用方式

```bash
pip install -r requirements.txt
python prepare_kaggle_data.py
python collect_mohrss_jobs.py --pages-per-province 80 --workers 8
python build_project_dataset.py
python pipeline.py --input data/project_jobs_real.csv --output output
python export_dashboard_data.py
```

当前真实快照由 `data/project_jobs_real.csv` 提供，包含 Kaggle 两个数据集和中国公共招聘网采集结果，共 37772 条岗位记录，其中中国公共招聘网 36398 条。大陆 31 个省级区域均有真实岗位样本；澳门、台湾暂无同口径岗位样本，页面显示为样本不足，不用虚构数据补齐。

输出文件：

- `clean_jobs.csv`：清洗后的岗位明细
- `city_index.csv`：城市就业吸引力指数
- `province_index.csv`：省份就业热度指标
- `skill_keywords.csv`：技能关键词热度
- `salary_model.joblib`：随机森林薪资预测模型
- `model_metrics.json`：模型评估结果

如果有多个 CSV，可先合并为一个文件，或多次运行后再拼接输出。
