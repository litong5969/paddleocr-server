# PaddleOCR Server 使用说明

## 镜像获取与运行
- 推荐挂载模型缓存目录，避免重复下载：`-v /mnt/user/appdata/paddleocr/models:/root/.paddleocr`
- 环境变量：复制 `.env.example` 为 `.env`，容器内端口固定 5000，默认宿主端口 `5215`（GUI 与 API 共用），默认启用 GPU；按需调整 `HOST_PORT`、`OCR_USE_GPU`、`OCR_LANG`、`PADDLE_IMAGE_TAG` 等（详见 `docs/ENVIRONMENT_VARIABLES.md`）。
- 核心镜像：基于 `paddlepaddle/paddle:<PADDLE_IMAGE_TAG>`，可通过环境变量选择官方标签。
- GPU 运行：
  ```bash
  docker run -d --gpus all \
    -p 5215:5000 \
    -v /mnt/user/appdata/paddleocr/models:/root/.paddleocr \
    --name paddleocr-server \
    litong5969/paddleocr-server:cuda12.6
  ```
- CPU 运行（无 GPU 也可用同一镜像）：
  ```bash
  docker run -d \
    -p 5215:5000 \
    -v /mnt/user/appdata/paddleocr/models:/root/.paddleocr \
    --name paddleocr-server \
    litong5969/paddleocr-server:cuda12.6
  ```
- docker compose 运行（使用 `.env` 配置端口/语言/GPU）：
  ```bash
  docker compose --compatibility up -d --build
  ```
  自定义端口示例：`HOST_PORT=5215 docker compose --compatibility up -d --build`
- 同步发布了 `:latest` 标签，等价于当前版本。

## API
- 端点：
  - `POST /ocr` — 图像 OCR 提取
  - `POST /ocr/batch` — 批量 OCR（表单多文件 `files`）
  - `GET /healthz` — 存活检查（始终 200）
  - `GET /readyz` — 就绪检查（OCR 引擎可用时 200，否则 503）
  - `GET /meta` — 运行时元信息（语言、版本、GPU/缓存目录）
  - `GET /metrics` — Prometheus 指标（默认开启，可通过 `METRICS_ENABLED=false` 关闭）

## 轻量 Web GUI（内置于同一镜像）
- 访问路径：`/ui`（根路径 `/` 已重定向到 `/ui`）
- 功能：
  - 拖拽/选择图片（支持多张） → 自动调用 `POST /ocr` 或 `POST /ocr/batch`
  - 展示识别文本与逐行置信度；支持“一键复制文本”
  - 一键导出文本（下载为 .txt）
  - 历史记录（最近 5 次，存储于本地浏览器，可清空）
- 定位：单页原生 HTML/JS，不引入重量前端框架，不增加镜像体积
- 示例：浏览器打开 `http://localhost:${HOST_PORT:-5215}/` 即可使用
- 截图：docs/summary/ui-screenshot.png（默认占位，运行脚本可生成真实截图）
- 请求（表单上传）：
  ```bash
  curl -X POST http://localhost:5215/ocr \
    -F "file=@/path/to/image.jpg"
  ```
- 返回（JSON Schema）：
  ```json
  {
    "text": "合并后的整段文本",
    "lines": [
      {"text": "每行文本", "score": 0.99}
    ]
  }
  ```
  - 不支持的 Content-Type（非 image/*）返回 415
  - OCR 引擎未就绪返回 503

## 健康检查与观测
- `GET /healthz`：用于存活探针；响应头 `X-Process-Time-ms` 提供服务端处理耗时（毫秒）。
- `GET /readyz`：用于就绪探针；当模型尚未加载或 PaddleOCR 不可用时返回 503。
- `GET /meta`：返回当前配置（`OCR_LANG`/`OCR_VERSION`/`OCR_USE_GPU`/`PADDLEOCR_HOME`）。
- `GET /metrics`：暴露 Prometheus 指标（含 `http_request_latency_seconds`、`ocr_inference_seconds`、`ocr_requests_total` 等）；默认启用，可通过 `METRICS_ENABLED=false` 关闭。

## 性能与批处理
- 冷启动优化：默认在进程启动后进行一次轻量 warmup（10x10 黑图），可通过 `OCR_WARMUP_ON_START=false` 关闭；超时控制 `OCR_WARMUP_TIMEOUT_SEC`（默认 20）。
- 批处理：`POST /ocr/batch` 接收多文件字段名 `files`，最多 `OCR_BATCH_MAX_FILES`（默认 8），返回每个文件的 `filename/text/lines`。

## 上传限制与安全
- 单文件大小：`MAX_IMAGE_SIZE_MB`（默认 10MB），超过返回 413。
- 批量总大小：`MAX_BATCH_TOTAL_MB`（默认 20MB），超过返回 413。
- Content-Type：限制为 `image/*`，不合规返回 415。

## 基准测试
- 依赖：宿主机安装 `python3` 与 `pip`，并确保服务已启动。
- 脚本：`python scripts/bench/bench_ocr.py --url http://localhost:5215/ocr --image test.jpg --concurrency 4 --requests 16`
- 输出：打印 p50/p95/p99、平均耗时、成功/失败数，可用于对比不同镜像标签/参数的性能。

## 开发测试
- 容器内运行（推荐）：
  ```bash
  docker compose run --rm paddleocr-server bash -lc "scripts/dev/run_tests.sh"
  ```
- 本地运行（需本机 Python）：
  ```bash
  ./scripts/dev/run_tests.sh
  ```

## Kubernetes 部署
- Kustomize（CPU 默认）：
  ```bash
  kubectl apply -k ops/k8s/base
  ```
- Kustomize（GPU overlay，需要部署 NVIDIA device plugin）：
  ```bash
  kubectl apply -k ops/k8s/gpu
  ```
- 调整镜像：编辑 `ops/k8s/base/kustomization.yaml` 的 `images` 或在 apply 前覆盖。

### Ingress 路径路由（推荐同端口）
- `ops/k8s/base/ingress.yaml` 已包含示例，将 `/`（含 `/ui`）与 `/ocr` 路径指向同一 Service 端口。
- Helm Chart 也支持 Ingress（`ops/helm/paddleocr-server/templates/ingress.yaml`）。

### Nginx 反向代理（同源示例）
- 参考：`docs/ops/NGINX_PATH_ROUTING.md`

## Helm Chart 部署
- 本地安装（CPU）：
  ```bash
  helm upgrade -i ocr ./ops/helm/paddleocr-server \
    --set image.repository=ghcr.io/litong5969/paddleocr-server \
    --set image.tag=latest \
    --set env.OCR_USE_GPU=false
  ```
- GPU：
  ```bash
  helm upgrade -i ocr ./ops/helm/paddleocr-server \
    --set image.repository=ghcr.io/litong5969/paddleocr-server \
    --set image.tag=latest \
    --set useGpu=true --set env.OCR_USE_GPU=true
  ```

## CI/CD（GitHub Actions → GHCR）
- 工作流：`.github/workflows/docker-ghcr.yml`
- 触发：推送到 `main` 自动构建并推送镜像到 `ghcr.io/litong5969/paddleocr-server:latest` 与 `:<sha>`
- 可通过 `Repository variables` 自定义 `PADDLE_IMAGE_TAG`

## 开发与发布
- 修改代码后直接 `git add . && git commit -m "..." && git push` 到 `main`。
- GitHub Actions 会自动构建并推送镜像到 DockerHub：`litong5969/paddleocr-server:{latest,cuda12.6}`。
