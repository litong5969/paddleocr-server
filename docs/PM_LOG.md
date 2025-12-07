# PM_LOG

- 2024-12-07: Temporary Bootstrap 启动，执行 `scripts/team-integrity-check/run_team_integrity_check.sh`，结果 PASS。
- 2024-12-07: research/TaskBook.md 补充定位、目标用户、价值命题、竞品、MVP 范围与风险评估。
- 2024-12-07: Integrity: OK; Research: OK; Planning: OK; Ready to load PM_BOOTSTRAP。
- 2024-12-07: temporary_bootstrap completed and archived；下一步按 docs/INFRA_SETUP_GUIDE.md 初始化基础设施并切换至 docs/governance/PM_BOOTSTRAP.md 常态流程。
- 2024-12-07: 完成基础设施配置：新增 `.env.template`/.env 文件族与 `docs/ENVIRONMENT_VARIABLES.md`，引入 docker compose 启动脚本（`docker-compose.yml`），server 支持环境变量与 GPU/CPU 切换；当前服务无数据库/Redis 需求。
- 2024-12-07: 切换到 `docs/governance/PM_BOOTSTRAP.md` 常态工作流，后续任务按轻量治理基线执行。
- 2024-12-07: TTOS 记录：保留原 Docker 基础功能；默认对外端口 5213（GPU 优先）；核心镜像 `paddlepaddle/paddle` 版本可通过 `PADDLE_IMAGE_TAG` 选择。
- 2024-12-07: 本地开发环境使用 APP_PORT=5214，已通过 `docker compose --compatibility up -d --build` 启动 GPU 实例（Tesla P4），镜像标签 `3.2.2-gpu-cuda12.6-cudnn9.5`。

- 2025-12-07: 按 PM_BOOTSTRAP 启动新会话（session-001），建立 summary 与 pm_state，准备更新 KANBAN；执行团队自检脚本以作为 summary-validator/selfcheck 依据（结果 PASS）。

- 2025-12-07: MVP-001 推进：
  - 代码：增强 `server.py`，新增 `/healthz` `/readyz` `/meta`，`/ocr` 提供明确响应模型与错误处理，加入请求耗时头 `X-Process-Time-ms`，并在 PaddleOCR 不可用或 GPU 初始化失败时自动 CPU 回退或返回 503（就绪未通过）。
  - 文档：`README.md` 增补 API 规范（端点与返回 Schema、探针与元信息）。
  - 验证：添加最小测试 `tests/test_api.py`（使用 FakeOCR 绕过重量依赖）；未在本环境中执行重载模型测试。
  - 看板：更新 KANBAN，标记 /ocr 最小实现切片已落地。

- 2025-12-07: PERF-001 推进：
  - 冷启动优化：新增启动 warmup（10x10 图像），可通过 `OCR_WARMUP_ON_START` 关闭；`OCR_WARMUP_TIMEOUT_SEC` 控制保护时长。
  - 批处理：新增 `POST /ocr/batch`（多文件 `files`，最大 `OCR_BATCH_MAX_FILES`，默认 8）。
  - 观测：集成 Prometheus 指标 `/metrics`（`METRICS_ENABLED` 可关），提供 `http_request_latency_seconds`、`ocr_inference_seconds`、`ocr_requests_total` 等；中间件记录端点延迟。
  - 依赖：`prometheus-client` 写入 `requirements.txt`。
  - 文档/环境：更新 `README.md` 与 `docs/ENVIRONMENT_VARIABLES.md`，补充相关变量说明；同步 `.env.*` 模板。
  - 测试：新增 `tests/test_batch_and_metrics.py` 覆盖批处理与指标暴露最小路径。

- 2025-12-07: 安全/限制与基准：
  - 上传限制：`MAX_IMAGE_SIZE_MB`、`MAX_BATCH_TOTAL_MB`，服务端流式写入临时文件并在阈值处返回 413；新增 PIL 检测图像尺寸以记录像素规模直方图。
  - 基准脚本：`scripts/bench/bench_ocr.py`，支持 `--concurrency/--requests/--image/--url`，输出 p50/p95/p99 等指标。
  - 测试：扩展 `tests/test_batch_and_metrics.py` 覆盖大小限制错误路径。

- 2025-12-08: 交付与部署增强：
  - K8s：新增 Kustomize base（CPU）与 GPU overlay，包含 Deployment/Service、就绪/存活探针与缓存卷挂载。
  - Helm：新增 Chart（ops/helm/paddleocr-server），支持 `useGpu`、持久化缓存 PVC、Ingress、镜像仓库与环境变量配置。
  - CI：新增 GitHub Actions 工作流 `.github/workflows/docker-ghcr.yml`，推送镜像至 `ghcr.io/<owner>/<repo>`，支持 `vars.PADDLE_IMAGE_TAG`。
  - 文档：README 增补 K8s/Helm/CI 用法与镜像覆盖指引。

- 2025-12-08: GUI 目标落地：
  - 设计：`docs/design/GUI_DESIGN.md` 说明轻量实现方案（StaticFiles + 单页 HTML/JS），与 REST API 共存于同一镜像。
  - 实现：`web/ui/index.html` 单页 GUI，支持拖拽/选择图片，调用 `/ocr` 并展示文本/置信度。
  - 集成：`server.py` 挂载 `/ui`，根路径 `/` 重定向至 `/ui`；`Dockerfile` 复制 `web` 目录。
  - 文档：`README.md` 新增 Web GUI 使用说明与截图占位；`ROADMAP.md` 增加 Q1 目标条目；`KANBAN.md` 新增 GUI 任务链。

- 2025-12-08: GUI 增强（按建议完成）：
  - 复制按钮：支持一键复制识别文本。
  - 历史记录：最近 5 次结果存储在浏览器 LocalStorage，可点击回看、可清空。
  - 多文件：input 支持 multiple，拖拽多图；批量自动调用 `/ocr/batch` 并分节展示每张图片结果。
  - 导出：新增“导出文本”按钮，下载聚合文本为 .txt。
  - 截图：新增 `docs/summary/ui-screenshot.svg` 并在 README 引用；补充 `docs/sop/CAPTURE_UI_SCREENSHOT.md` 指南用于生成真实 PNG 截图。
  - 元信息：GUI 显示服务信息（/meta + /readyz），包含 language/version/GPU/cache/metrics/ready。
 - 2025-12-08: GUI 参数面板与截图脚本：
   - 参数面板：调用模式（自动/单图/批量）、置信度阈值、最多行数、聚合分隔符；偏好持久化至 LocalStorage。
   - 截图脚本：`scripts/dev/capture_ui_screenshot.sh` 基于 Chrome/Chromium 生成 PNG 截图；更新 SOP 文档使用脚本。
- 2025-12-08: 端口更新：将 GUI/API 默认宿主端口调整为 5215（`HOST_PORT` 可覆盖）；更新 docker-compose、环境模板与 README 示例、基准脚本默认 URL。

- 2025-12-08: 路径路由示例补充：
  - K8s：`ops/k8s/base/ingress.yaml` 将 `/`（含 `/ui`）与 `/ocr` 路径转发至同一 Service 端口。
  - Nginx：新增 `docs/ops/NGINX_PATH_ROUTING.md`，提供本机或边缘网关的同源代理配置示例。

- 2025-12-08: GHCR 仓库对齐与交付工件：
  - GHCR 仓库：使用 `ghcr.io/litong5969/paddleocr-server`（Helm values 与 README 示例已替换）。
  - 截图：新增占位 PNG `docs/summary/ui-screenshot.png`，可用脚本生成真实截图替换。
  - 基准：新增 `docs/summary/bench-2025-12-08.md`，提供测试命令与结果记录模板。

- 2025-12-08: CI 冒烟：新增 `.github/workflows/ci-smoke.yml`，包含：
  - unit：最小依赖（不安装 PaddleOCR）运行 pytest 覆盖 UI/API 关键路径（FakeOCR）。
  - python-smoke：最小依赖启动 uvicorn 服务，检查 `/healthz` 与 `/ui`；`/readyz` 非致命。
