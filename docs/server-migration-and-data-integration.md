# EmploySight 服务器迁移与真实数据接入说明

本文档用于把 EmploySight 项目迁移到 Linux 服务器运行，并保证页面展示的是项目真实岗位数据，而不是测试样例数据。

如果服务器计划使用 Docker / Docker Compose 部署，优先阅读 `docs/docker-deployment.md`。

## 1. 当前项目运行方式

项目由三部分组成：

| 模块 | 目录 | 作用 |
| --- | --- | --- |
| 前端 | `frontend/` | Vue 3 + TypeScript + ECharts，生产环境构建为静态文件 |
| 后端 | `backend/` | Python FastAPI，提供 `/api` 接口 |
| 数据处理 | `data-processing/` | 清洗真实岗位 CSV、生成指标、训练薪资模型、导出前后端快照 |

当前后端接口使用的是“真实数据快照模式”：

```text
data-processing/data/project_jobs_real.csv
  -> data-processing/export_dashboard_data.py
  -> backend/app/services/demo_data.py
  -> frontend/src/services/mockData.ts
```

注意：`demo_data.py` 和 `mockData.ts` 文件名保留为兼容旧代码，但内容已经由真实岗位快照生成。不要只看文件名就认为它是假数据。

当前真实快照指标：

| 指标 | 当前值 |
| --- | --- |
| 真实岗位记录 | 37772 |
| 有效薪资样本 | 37380 |
| 覆盖城市 | 350 |
| 可上图城市 | 44 |
| 有样本省级区域 | 32 |
| 样本不足区域 | 澳门、台湾 |
| 平均月薪 | 5681 |

这些值来自：

```text
data-processing/data/dashboard_snapshot_metadata.json
data-processing/data/project_jobs_real_metadata.json
```

## 2. 推荐服务器环境

建议使用 Ubuntu 22.04 / 24.04，其他 Linux 发行版命令类似。

```bash
sudo apt update
sudo apt install -y git nginx python3 python3-venv python3-pip nodejs npm
```

建议版本：

| 工具 | 建议版本 |
| --- | --- |
| Python | 3.10+ |
| Node.js | 18+ 或 20+ |
| Nginx | 系统仓库版本即可 |
| MySQL | 可选，8.0+ |

本项目没有根目录 `package.json`，前端命令必须进入 `frontend/` 后执行。

## 3. 拉取项目代码

建议部署目录：

```bash
sudo mkdir -p /opt/employsight
sudo chown -R $USER:$USER /opt/employsight
cd /opt/employsight
git clone https://github.com/Moyu52/EmploySight.git
cd EmploySight
```

检查真实数据文件是否存在：

```bash
ls -lh data-processing/data/project_jobs_real.csv
ls -lh data-processing/data/dashboard_snapshot_metadata.json
ls -lh backend/app/services/demo_data.py
ls -lh frontend/src/services/mockData.ts
```

如果 `project_jobs_real.csv` 不存在，页面仍可能能打开，但不能保证后续刷新数据。必须先补齐真实 CSV。

## 4. 安装后端和数据处理依赖

```bash
cd /opt/employsight/EmploySight
python3 -m venv /opt/employsight/venv
source /opt/employsight/venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
pip install -r data-processing/requirements.txt
```

后端可选环境文件：

```bash
cat > backend/.env <<'EOF'
APP_NAME=employsight
DEMO_MODE=true
MODEL_VERSION=random-forest-real-snapshot-v1
MYSQL_URL=mysql+pymysql://root:your_password@127.0.0.1:3306/graduate_employment?charset=utf8mb4
EOF
```

说明：

- 当前接口默认使用 `backend/app/services/demo_data.py` 中的真实快照数据。
- `MYSQL_URL` 是后续数据库查询接入预留项；当前不配置 MySQL 也能使用真实快照运行。
- 如果后续要求接口必须直接查 MySQL，需要替换 `backend/app/services/demo_data.py` 的读取逻辑为 SQLAlchemy 查询。

## 5. 真实数据接入与刷新

### 5.1 使用项目已有真实数据

如果服务器只需要运行当前版本，直接确认真实快照即可：

```bash
cd /opt/employsight/EmploySight
python3 - <<'PY'
import json
from pathlib import Path

meta = json.loads(Path("data-processing/data/dashboard_snapshot_metadata.json").read_text(encoding="utf-8"))
print(meta)
PY
```

应看到类似结果：

```text
rows: 37772
salary_rows: 37380
covered_cities: 350
regions_without_samples: ['澳门', '台湾']
```

### 5.2 重新接入新真实数据

如果你换了新的岗位数据，按下面流程重新生成前后端快照。

第一步：把真实岗位 CSV 放到：

```text
data-processing/data/project_jobs_real.csv
```

CSV 至少应包含这些字段中的一部分，脚本会按别名自动识别：

| 统一字段 | 常见字段名 |
| --- | --- |
| 岗位名称 | `job_title`、`title`、`岗位名称`、`职位名称` |
| 公司名称 | `company_name`、`company`、`公司名称` |
| 城市 | `city`、`work_city`、`工作城市` |
| 省份 | `province`、`work_province`、`工作省份` |
| 薪资 | `salary`、`salary_range`、`薪资` |
| 学历 | `education`、`学历要求` |
| 经验 | `experience`、`经验要求` |
| 行业 | `industry`、`行业类别` |
| 发布时间 | `publish_date`、`发布时间`、`date` |
| 岗位描述 | `description`、`job_description`、`岗位描述` |

第二步：运行清洗、聚合和模型训练：

```bash
cd /opt/employsight/EmploySight/data-processing
source /opt/employsight/venv/bin/activate
python pipeline.py --input data/project_jobs_real.csv --output output
```

这一步会生成：

```text
data-processing/output/clean_jobs.csv
data-processing/output/city_index.csv
data-processing/output/province_index.csv
data-processing/output/skill_keywords.csv
data-processing/output/model_metrics.json
data-processing/output/salary_model.joblib
```

第三步：把真实数据导出到后端接口快照和前端兜底数据：

```bash
cd /opt/employsight/EmploySight/data-processing
python export_dashboard_data.py
```

这一步很关键。只运行 `pipeline.py` 不会自动更新页面接口数据；必须运行 `export_dashboard_data.py`。

它会重写：

```text
backend/app/services/demo_data.py
frontend/src/services/mockData.ts
data-processing/data/dashboard_snapshot_metadata.json
```

第四步：刷新前端构建并重启后端：

```bash
cd /opt/employsight/EmploySight/frontend
npm ci
npm run build

sudo systemctl restart employsight-backend
sudo systemctl reload nginx
```

因为 `mockData.ts` 会被打包进前端，所以每次重新导出数据后都要重新 `npm run build`。

## 6. 启动后端

先手动验证：

```bash
cd /opt/employsight/EmploySight/backend
source /opt/employsight/venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

另开一个终端检查：

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/dashboard/overview
```

生产环境建议使用 systemd：

```bash
sudo tee /etc/systemd/system/employsight-backend.service > /dev/null <<'EOF'
[Unit]
Description=EmploySight FastAPI Backend
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/employsight/EmploySight/backend
EnvironmentFile=-/opt/employsight/EmploySight/backend/.env
ExecStart=/opt/employsight/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
```

启动：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now employsight-backend
sudo systemctl status employsight-backend
```

查看日志：

```bash
journalctl -u employsight-backend -f
```

## 7. 构建前端

```bash
cd /opt/employsight/EmploySight/frontend
npm ci
npm run build
```

构建产物在：

```text
frontend/dist/
```

不要在项目根目录执行 `npm install` 或 `npm run build`，根目录没有 Node 项目配置。

## 8. 配置 Nginx

创建站点配置：

```bash
sudo tee /etc/nginx/sites-available/employsight > /dev/null <<'EOF'
server {
    listen 80;
    server_name your_domain_or_server_ip;

    root /opt/employsight/EmploySight/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
```

启用配置：

```bash
sudo ln -sf /etc/nginx/sites-available/employsight /etc/nginx/sites-enabled/employsight
sudo nginx -t
sudo systemctl reload nginx
```

如果有默认站点冲突，可以删除默认配置链接：

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

## 9. 真实数据验证清单

部署后必须做下面几项检查。

### 9.1 检查后端接口返回真实快照

```bash
curl -s http://127.0.0.1:8000/api/dashboard/overview | python3 -c '
import json, sys
body = json.load(sys.stdin)
data = body["data"]
print("totalJobs =", data["totalJobs"])
print("salarySampleRows =", data["salarySampleRows"])
print("coveredCities =", data["coveredCities"])
print("publishStart =", data["publishStart"])
print("publishEnd =", data["publishEnd"])
'
```

当前版本应接近：

```text
totalJobs = 37772
salarySampleRows = 37380
coveredCities = 350
publishEnd = 2026-05-19
```

如果这些值变成很小的样例值，说明没有接入真实数据。

### 9.2 检查 Nginx 是否正确转发 API

```bash
curl -s http://your_domain_or_server_ip/api/health
curl -s http://your_domain_or_server_ip/api/dashboard/overview
```

如果本机 `127.0.0.1:8000` 正常，但域名 `/api` 不正常，问题在 Nginx 反向代理。

### 9.3 检查前端没有只跑静态兜底

浏览器访问：

```text
http://your_domain_or_server_ip
```

然后打开浏览器开发者工具 Network，确认这些请求返回 200：

```text
/api/dashboard/overview
/api/dashboard/provinces
/api/dashboard/cities/ranking
/api/dashboard/analysis
/api/dashboard/live-jobs
```

前端代码在接口失败时会使用 `frontend/src/services/mockData.ts` 的兜底数据。兜底数据本身也是由真实快照生成的，但生产环境仍然建议保证 `/api` 正常返回，方便后续更新数据。

## 10. MySQL 接入说明

当前仓库提供了 MySQL 表结构：

```text
database/schema.sql
database/seed.sql
```

初始化数据库：

```bash
mysql -uroot -p < database/schema.sql
mysql -uroot -p graduate_employment < database/seed.sql
```

注意：

- `database/seed.sql` 只是初始化样例，不是真实岗位分析数据。
- 当前 FastAPI 大屏接口默认不从 MySQL 查询，而是从 `backend/app/services/demo_data.py` 读取真实聚合快照。
- 如果要把所有真实岗位明细写入 MySQL，可以先运行 `pipeline.py` 生成 `output/clean_jobs.csv`，再按 `database/schema.sql` 字段写导入脚本或使用 `LOAD DATA LOCAL INFILE`。
- 如果要让接口直接查 MySQL，需要新增 Repository/Service 查询逻辑，替换 `app/routers/dashboard.py` 当前引用的快照函数。

推荐迁移阶段先使用“真实快照模式”上线，稳定后再做 MySQL 查询改造。这样风险最低，也能保证服务器运行时展示真实数据。

## 11. 常见问题

### 页面能打开，但数据明显不对

按顺序检查：

```bash
cat data-processing/data/dashboard_snapshot_metadata.json
curl -s http://127.0.0.1:8000/api/dashboard/overview
curl -s http://your_domain_or_server_ip/api/dashboard/overview
```

如果元数据正确但后端接口不正确，检查是否重启了 `employsight-backend`。

### 更新 CSV 后页面仍然是旧数据

通常是漏了其中一步：

```bash
cd data-processing
python pipeline.py --input data/project_jobs_real.csv --output output
python export_dashboard_data.py

cd ../frontend
npm run build

sudo systemctl restart employsight-backend
sudo systemctl reload nginx
```

### 只导入 MySQL 后页面没有变化

这是当前设计决定的。现有接口读取的是真实快照文件，不是 MySQL。导入 MySQL 不会自动改变页面展示，除非你实现后端 MySQL 查询服务。

### 前端开发模式可以访问接口，生产环境访问不到

开发模式依赖 `frontend/vite.config.ts` 的代理：

```text
/api -> http://localhost:8000
```

生产环境没有 Vite 代理，必须由 Nginx 配置 `/api/` 反向代理到 `127.0.0.1:8000`。

## 12. 迁移完成检查表

上线前逐项确认：

- [ ] 代码已拉取到服务器。
- [ ] `data-processing/data/project_jobs_real.csv` 存在。
- [ ] `data-processing/data/dashboard_snapshot_metadata.json` 中记录数正常。
- [ ] `backend/app/services/demo_data.py` 已由真实数据生成。
- [ ] `frontend/src/services/mockData.ts` 已由真实数据生成。
- [ ] 后端依赖安装完成。
- [ ] `curl http://127.0.0.1:8000/api/health` 返回正常。
- [ ] `curl http://127.0.0.1:8000/api/dashboard/overview` 返回真实岗位数量。
- [ ] 前端已在 `frontend/` 下完成 `npm ci && npm run build`。
- [ ] Nginx `root` 指向 `frontend/dist`。
- [ ] Nginx `/api/` 已反代到 `127.0.0.1:8000`。
- [ ] 浏览器 Network 中 `/api/dashboard/*` 请求返回 200。
- [ ] 页面显示岗位样本、城市覆盖、薪资样本等真实指标。
