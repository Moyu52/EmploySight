# 数据处理与模型训练

该目录用于处理 Kaggle 中国招聘岗位数据：

- `China Jobs Data`
- `Job Posting Data in China`

脚本会完成字段映射、薪资解析、学历经验标准化、城市吸引力指数、应届生友好度、技能关键词热度和薪资预测模型训练。

## 使用方式

```bash
pip install -r requirements.txt
python pipeline.py --input data/jobs.csv --output output
```

输出文件：

- `clean_jobs.csv`：清洗后的岗位明细
- `city_index.csv`：城市就业吸引力指数
- `province_index.csv`：省份就业热度指标
- `skill_keywords.csv`：技能关键词热度
- `salary_model.joblib`：随机森林薪资预测模型
- `model_metrics.json`：模型评估结果

如果有多个 CSV，可先合并为一个文件，或多次运行后再拼接输出。
