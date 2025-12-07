# ENVIRONMENT_VARIABLES

| 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| `APP_HOST` | `0.0.0.0` | Uvicorn 监听地址 |
| `APP_PORT` | `5000` | 容器内 Uvicorn 监听端口 |
| `HOST_PORT` | `5215` | 宿主机映射端口（默认为 GUI 端口） |
| `PADDLE_IMAGE_TAG` | `3.2.2-gpu-cuda12.6-cudnn9.5` | 构建时使用的 `paddlepaddle/paddle` 标签，可替换为官方标签列表 |
| `OCR_LANG` | `ch` | PaddleOCR 语言配置 |
| `OCR_VERSION` | `PP-OCRv4` | PaddleOCR 模型版本 |
| `OCR_USE_ANGLE_CLS` | `true` | 是否启用文字方向分类 |
| `OCR_USE_GPU` | `true` | 是否启用 GPU 推理（需要宿主机 GPU 与驱动，可设为 false 退回 CPU） |
| `PADDLEOCR_HOME` | `/root/.paddleocr` | PaddleOCR 模型缓存路径，建议挂载到宿主机避免重复下载 |
| `METRICS_ENABLED` | `true` | 是否启用 Prometheus 指标 `/metrics` |
| `OCR_WARMUP_ON_START` | `true` | 启动后是否进行一次轻量 warmup（加速首次请求）|
| `OCR_WARMUP_TIMEOUT_SEC` | `20` | warmup 超时秒数（保护性）|
| `OCR_BATCH_MAX_FILES` | `8` | 批量接口 `/ocr/batch` 单次最大文件数 |
| `MAX_IMAGE_SIZE_MB` | `10` | 单张图片最大体积（MB） |
| `MAX_BATCH_TOTAL_MB` | `20` | 批量请求总体积上限（MB） |

所有环境文件字段保持与 `.env.template` 对齐：`.env` / `.env.dev` / `.env.example` 均包含上述键，未新增额外字段。
开发场景使用 `.env.dev` 将 `HOST_PORT` 设置为 `5214`（内部端口仍为 5000）。
