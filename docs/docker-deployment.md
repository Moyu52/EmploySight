# EmploySight Docker 容器部署说明

本文档用于在服务器上通过 Docker 部署 EmploySight，并说明部署前如何检测软件是否已安装、缺什么补什么，以及如何确认项目使用的是真实岗位数据。

## 1. Docker 部署方式说明

本仓库已经提供 Docker 部署文件：

| 文件 | 作用 |
| --- | --- |
| `docker-compose.yml` | 编排前端、后端、可选 MySQL、可选数据刷新容器 |
| `backend/Dockerfile` | 构建 FastAPI 后端镜像 |
| `frontend/Dockerfile` | 构建 Vue 前端并用 Nginx 容器运行 |
| `deploy/nginx/employsight.conf` | 前端容器内 Nginx 配置，负责静态页面和 `/api` 反代 |
| `.dockerignore` | 减少 Docker 构建上下文，排除缓存、截图、临时文件 |

默认容器结构：

```text
用户浏览器
  -> frontend 容器 Nginx:80
    -> 静态页面 frontend/dist
    -> /api 反向代理到 backend:8000
  -> backend 容器 FastAPI
```

当前项目默认使用“真实数据快照模式”，不强制依赖 MySQL：

```text
data-processing/data/project_jobs_real.csv
  -> data-processing/export_dashboard_data.py
  -> backend/app/services/demo_data.py
  -> frontend/src/services/mockData.ts
```

MySQL 容器已经写在 `docker-compose.yml` 里，但默认不会启动。需要数据库时再用 `--profile mysql` 启动。

上线前建议修改 `docker-compose.yml` 里的 MySQL 默认密码：

```yaml
MYSQL_ROOT_PASSWORD: root_password_change_me
MYSQL_PASSWORD: employsight_password
```

当前后端默认不直接读取 MySQL，但不要把默认密码用于公开服务器的生产数据库。

## 2. 服务器软件检测

先进入服务器，执行下面检测命令。

```bash
echo "=== 系统信息 ==="
cat /etc/os-release 2>/dev/null || uname -a

echo "=== Git ==="
if command -v git >/dev/null 2>&1; then
  git --version
else
  echo "Git 未安装"
fi

echo "=== Docker ==="
if command -v docker >/dev/null 2>&1; then
  docker --version
else
  echo "Docker 未安装"
fi

echo "=== Docker Compose ==="
if docker compose version >/dev/null 2>&1; then
  docker compose version
else
  echo "Docker Compose 插件未安装"
fi

echo "=== 宿主机 MySQL，可选 ==="
if command -v mysql >/dev/null 2>&1; then
  mysql --version
else
  echo "宿主机 MySQL 未安装；Docker 部署可直接使用 MySQL 容器"
fi

echo "=== 宿主机 Python，可选 ==="
if command -v python3 >/dev/null 2>&1; then
  python3 --version
else
  echo "宿主机 Python 未安装；Docker 部署不需要宿主机 Python"
fi

echo "=== 宿主机 Node.js，可选 ==="
if command -v node >/dev/null 2>&1; then
  node -v
else
  echo "宿主机 Node.js 未安装；Docker 部署不需要宿主机 Node.js"
fi

echo "=== 端口占用 ==="
sudo ss -tulpen | grep -E ':(80|8000|3306)\s' || echo "80/8000/3306 未发现监听占用"
```

判断原则：

| 软件 | Docker 部署是否必须装在宿主机 | 说明 |
| --- | --- | --- |
| Git | 建议安装 | 用于拉取代码 |
| Docker | 必须 | 运行容器 |
| Docker Compose 插件 | 必须 | 运行 `docker compose` |
| Python | 不必须 | 后端和数据处理可在容器里跑 |
| Node.js | 不必须 | 前端构建可在容器里跑 |
| Nginx | 不必须 | 前端容器自带 Nginx |
| MySQL | 不必须 | 需要数据库时用 MySQL 容器即可 |

## 3. 安装缺失软件

### 3.1 安装 Git

如果 `git --version` 不存在：

```bash
sudo apt update
sudo apt install -y git
```

### 3.2 安装 Docker 和 Compose 插件

如果 `docker --version` 或 `docker compose version` 不存在，Ubuntu 服务器建议使用 Docker 官方源安装：

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

启动 Docker：

```bash
sudo systemctl enable --now docker
docker --version
docker compose version
```

如果不想每次都加 `sudo`：

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 3.3 MySQL 是否需要安装

Docker 部署下不建议直接在宿主机安装 MySQL，除非你明确要让其他项目共用宿主机数据库。

推荐做法：

```bash
docker compose --profile mysql up -d mysql
```

如果确实要安装宿主机 MySQL：

```bash
sudo apt update
sudo apt install -y mysql-server
sudo systemctl enable --now mysql
mysql --version
```

但要注意：当前 EmploySight 后端默认读取真实快照文件，不直接查 MySQL。只安装 MySQL 不会自动改变页面数据。

## 4. 拉取项目

```bash
sudo mkdir -p /opt/employsight
sudo chown -R $USER:$USER /opt/employsight
cd /opt/employsight
git clone https://github.com/Moyu52/EmploySight.git
cd EmploySight
```

检查关键文件：

```bash
ls -lh docker-compose.yml
ls -lh backend/Dockerfile
ls -lh frontend/Dockerfile
ls -lh deploy/nginx/employsight.conf
ls -lh data-processing/data/project_jobs_real.csv
ls -lh data-processing/data/dashboard_snapshot_metadata.json
```

如果 `project_jobs_real.csv` 不存在，说明真实数据文件没有带到服务器，需要先补齐。

## 5. 启动基础版本

基础版本只启动前端和后端，不启动 MySQL：

```bash
cd /opt/employsight/EmploySight
docker compose up -d --build
```

查看容器：

```bash
docker compose ps
```

查看日志：

```bash
docker compose logs -f backend
docker compose logs -f frontend
```

访问：

```text
http://服务器IP/
```

后端本机检查：

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/dashboard/overview
```

前端容器反代检查：

```bash
curl http://127.0.0.1/api/health
curl http://127.0.0.1/api/dashboard/overview
```

如果服务器 80 端口已经被宿主机 Nginx 或其他服务占用，可以把 `docker-compose.yml` 里的：

```yaml
ports:
  - "80:80"
```

改成：

```yaml
ports:
  - "8080:80"
```

然后访问：

```text
http://服务器IP:8080/
```

## 6. 启动 MySQL 容器

如果你要同时准备 MySQL 容器：

```bash
cd /opt/employsight/EmploySight
docker compose --profile mysql up -d mysql
```

第一次启动时会执行：

```text
database/schema.sql
database/seed.sql
```

注意：

- `database/seed.sql` 是数据库初始化样例，不是当前页面使用的真实岗位分析数据。
- MySQL 容器默认只监听宿主机 `127.0.0.1:3306`，外网不能直接访问。
- 数据保存在 Docker volume `employsight-mysql-data`。

进入数据库：

```bash
docker compose exec mysql mysql -uemploysight -pemploysight_password graduate_employment
```

如果你修改了初始化 SQL，并希望重新初始化数据库：

```bash
docker compose --profile mysql down
docker volume rm employsight_employsight-mysql-data
docker compose --profile mysql up -d mysql
```

这会删除 MySQL 容器数据，生产环境不要随便执行。

## 7. 用 Docker 刷新真实数据

如果服务器没有 Python，也可以直接用 Docker 运行数据处理。

第一步：替换或上传新的真实数据：

```text
data-processing/data/project_jobs_real.csv
```

第二步：运行数据刷新容器：

```bash
cd /opt/employsight/EmploySight
docker compose --profile tools run --rm data-refresh
```

这会执行：

```bash
python pipeline.py --input data/project_jobs_real.csv --output output
python export_dashboard_data.py
```

并更新：

```text
data-processing/output/
data-processing/data/dashboard_snapshot_metadata.json
backend/app/services/demo_data.py
frontend/src/services/mockData.ts
```

如果生成文件变成 root 属主，可以修正权限：

```bash
sudo chown -R $USER:$USER \
  data-processing/output \
  data-processing/data/dashboard_snapshot_metadata.json \
  backend/app/services/demo_data.py \
  frontend/src/services/mockData.ts
```

第三步：重新构建前端和后端镜像：

```bash
docker compose up -d --build backend frontend
```

这一步不能省。因为：

- 后端镜像需要重新打包新的 `backend/app/services/demo_data.py`。
- 前端镜像需要重新打包新的 `frontend/src/services/mockData.ts`。

## 8. 验证是否接入真实数据

### 8.1 看元数据文件

```bash
cat data-processing/data/dashboard_snapshot_metadata.json
```

当前版本应接近：

```json
{
  "rows": 37772,
  "salary_rows": 37380,
  "covered_cities": 350,
  "mappable_cities": 44,
  "average_salary": 5681
}
```

### 8.2 看后端容器接口

```bash
curl -s http://127.0.0.1:8000/api/dashboard/overview | python3 -m json.tool | head -80
```

如果宿主机没有 Python，可以用后端容器里的 Python：

```bash
curl -s http://127.0.0.1:8000/api/dashboard/overview \
  | docker compose exec -T backend python -m json.tool \
  | head -80
```

重点看这些字段：

```text
totalJobs
salarySampleRows
coveredCities
publishStart
publishEnd
```

当前版本应接近：

```text
totalJobs = 37772
salarySampleRows = 37380
coveredCities = 350
publishEnd = 2026-05-19
```

如果这些值很小，通常说明你没有运行 `export_dashboard_data.py`，或者容器没有重新 build。

### 8.3 看前端请求

浏览器打开：

```text
http://服务器IP/
```

打开开发者工具 Network，确认这些接口返回 200：

```text
/api/dashboard/overview
/api/dashboard/provinces
/api/dashboard/cities/ranking
/api/dashboard/analysis
/api/dashboard/live-jobs
```

如果页面能打开，但这些接口失败，前端会使用打包时的 `mockData.ts` 兜底数据。兜底数据也是由真实快照生成的，但生产部署仍然应该保证 `/api` 正常。

## 9. 更新代码后的部署

```bash
cd /opt/employsight/EmploySight
git pull
docker compose up -d --build
```

如果同时要启动 MySQL：

```bash
docker compose --profile mysql up -d --build
```

如果只重启：

```bash
docker compose restart
```

如果要完全停止：

```bash
docker compose down
```

不要随便加 `-v`，否则会删除 MySQL volume。

## 10. 常见问题

### Docker 已安装，但 `docker compose` 不存在

说明缺少 Compose 插件：

```bash
sudo apt install -y docker-compose-plugin
docker compose version
```

### 80 端口被占用

检查：

```bash
sudo ss -tulpen | grep ':80'
```

处理方式二选一：

- 停掉宿主机 Nginx 或其他占用 80 的服务。
- 把 `docker-compose.yml` 的 `frontend` 端口改成 `8080:80`。

### MySQL 没有安装怎么办

Docker 部署不需要宿主机 MySQL。直接启动 MySQL 容器：

```bash
docker compose --profile mysql up -d mysql
```

当前页面数据不依赖 MySQL，MySQL 主要用于后续扩展为数据库查询模式。

### Python 没有安装怎么办

Docker 部署不需要宿主机 Python。后端容器自带 Python；刷新数据可以用：

```bash
docker compose --profile tools run --rm data-refresh
```

### Node.js 没有安装怎么办

Docker 部署不需要宿主机 Node.js。前端镜像构建阶段使用 `node:20-alpine`。

### 修改真实 CSV 后页面还是旧数据

按顺序执行：

```bash
docker compose --profile tools run --rm data-refresh
docker compose up -d --build backend frontend
docker compose restart
```

然后重新检查：

```bash
curl -s http://127.0.0.1/api/dashboard/overview
```

## 11. Docker 部署检查表

- [ ] `git --version` 正常，或已安装 Git。
- [ ] `docker --version` 正常。
- [ ] `docker compose version` 正常。
- [ ] `data-processing/data/project_jobs_real.csv` 存在。
- [ ] `data-processing/data/dashboard_snapshot_metadata.json` 指标正常。
- [ ] `docker compose up -d --build` 执行成功。
- [ ] `docker compose ps` 中 `frontend`、`backend` 为运行状态。
- [ ] `curl http://127.0.0.1:8000/api/health` 正常。
- [ ] `curl http://127.0.0.1/api/dashboard/overview` 返回真实岗位数量。
- [ ] 浏览器访问 `http://服务器IP/` 页面正常。
- [ ] 浏览器 Network 中 `/api/dashboard/*` 请求返回 200。
