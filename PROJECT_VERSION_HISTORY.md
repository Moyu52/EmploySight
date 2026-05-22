# 项目版本回退记录

这个文档用于记录可以回退的稳定版本。项目出现问题时，优先回到下面记录的稳定分支，不要直接删除代码或乱改历史提交。

## 当前稳定版

| 版本 | 稳定分支 | 标签 | 说明 |
| --- | --- | --- | --- |
| 第一版 | `stable/v1` | `v1.0.0` | 当前就业态势感知平台第一版，包含态势大屏、城市评估、薪资预测、技能挖掘、职业推荐、数据治理和前后端演示数据。 |
| 第二版 | `stable/v2` | `v2.0.0` | 扩充真实岗位数据到 37772 条，接入中国公共招聘网与 Kaggle 公开岗位数据，修正页面职业方向、薪资经验口径和数据真实性说明。 |
| 第三版 | `stable/v3` | `v3.0.3` | 完善毕业设计系统形态，加入登录入口、平台首页、模型评估、报告中心和系统管理；v3.0.3 接入 OpenRouter AI 推荐与薪资解释，修复默认跳过登录页问题，并同步 Docker 配置说明。 |
| 第四版 | `stable/v4` | `v4.0.0` | 增强管理员安全能力，加入登录 IP 审计删除确认、删除密码防爆破、临时封禁 IP、解除封禁 IP、PBKDF2 哈希密码校验，并优化首页右侧核心指标字号与布局。 |

## 版本更新说明

### v3.0.3

- 职业推荐接口接入 OpenRouter，可基于学生画像生成方向、理由、技能差距和行动建议。
- 薪资预测接口保留本地数值模型，AI 只生成解释和影响因素，避免直接改动预测区间。
- AI 未配置、余额不足、限流或模型不可用时，后端自动回退到本地规则结果。
- 首次访问默认进入登录页，点击“进入平台”后进入系统，退出后返回登录页。
- Docker Compose 增加 `AI_API_KEY`、`AI_MODEL`、`AI_ENABLED` 等后端环境变量。
- 前端版本号升级到 `3.0.3`。

### v4.0.0

- 管理员登录页明确区分普通用户和 `admin` 身份。
- 管理员平台状态页新增登录 IP 审计、删除记录确认、封禁 IP 列表和解除封禁操作。
- 删除审计记录密码连续输错达到上限后临时封禁当前请求 IP，防止暴力破解删除密码。
- 删除密码和解除封禁密码改为 PBKDF2-HMAC-SHA256 哈希校验，真实 pepper 与哈希只通过后端环境变量配置。
- Docker Compose 增加管理员安全环境变量，部署文档补充哈希配置要求。
- 首页右侧核心指标卡使用更大的标签、数字、单位和图标，匹配拉伸后的卡片高度。
- 前端版本号升级到 `4.0.0`。

## 回到第三版

只想查看第三版：

```powershell
git fetch origin
git switch stable/v3
```

如果要基于第三版重新开一个修复分支：

```powershell
git fetch origin
git switch -c fix/from-v3 stable/v3
```

## 回到第二版

只想查看第二版：

```powershell
git fetch origin
git switch stable/v2
```

如果要基于第二版重新开一个修复分支：

```powershell
git fetch origin
git switch -c fix/from-v2 stable/v2
```

## 回到第一版

只想查看第一版：

```powershell
git fetch origin
git switch stable/v1
```

如果要基于第一版重新开一个修复分支：

```powershell
git fetch origin
git switch -c fix/from-v1 stable/v1
```

如果确认要把 `main` 强制恢复到第一版，先备份当前工作，再执行：

```powershell
git fetch origin
git switch main
git reset --hard stable/v1
git push --force-with-lease origin main
```

## 自动推送记录

本仓库已配置本地 Git hook：`.githooks/pre-push`。以后每次执行 `git push` 时，hook 会把当前分支、提交号和远程地址追加到下面表格中。

注意：Git hook 是在本机 push 过程中写入本文档的，所以新增记录会先出现在本地工作区。如果希望 GitHub 上也保存这些记录，下一次提交时把本文档一起提交即可。

| 时间 | 类型 | 当前分支 | 提交 | 远程 |
| --- | --- | --- | --- | --- |
| 2026-05-19 10:56:05 +08:00 | 第一版稳定点 | `main` -> `stable/v1` | `v1.0.0` | `origin` |
| 2026-05-19 11:19:30 +08:00 | push | `main` | `483a102` | `https://github.com/Moyu52/New-project.git` |
| 2026-05-19 20:06:51 +08:00 | push | `main` | `0391efc` | `https://github.com/Moyu52/New-project.git` |
| 2026-05-20 23:43:22 +08:00 | push | `main` | `bc6e297` | `https://github.com/Moyu52/New-project.git` |
| 2026-05-20 23:44:49 +08:00 | push | `main` | `de296d3` | `https://github.com/Moyu52/New-project.git` |
| 2026-05-21 08:17:11 +08:00 | push | `main` | `dd80fe3` | `https://github.com/Moyu52/New-project.git` |
| 2026-05-22 10:47:32 +08:00 | push | `main` | `5a52764` | `https://github.com/Moyu52/EmploySight.git` |
| 2026-05-22 14:29:38 +08:00 | push | `main` | `ba3bd46` | `https://github.com/Moyu52/EmploySight.git` |
| 2026-05-22 15:39:32 +08:00 | push | `main` | `e3ae794` | `https://github.com/Moyu52/EmploySight.git` |
| 2026-05-22 18:02:46 +08:00 | push | `main` | `3a2ca9e` | `https://github.com/Moyu52/EmploySight.git` |
| 2026-05-22 18:03:12 +08:00 | push | `main` | `3a2ca9e` | `https://github.com/Moyu52/EmploySight.git` |
