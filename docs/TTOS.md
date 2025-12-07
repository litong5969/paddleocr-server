# TTOS 记录

1. 本项目是在原有 Docker 项目基础上升级，现有 Docker 最基本功能必须保留（保留 `POST /ocr` API、基础镜像启动与模型挂载能力）。  
2. Docker API 映射：容器内端口固定 `5000`，宿主机默认映射 `5215`（GUI 与 API 共用）；可通过 `HOST_PORT` 自定义。默认启用 GPU。  
3. 核心镜像来源 `paddlepaddle/paddle`，需提供可选版本：通过 `PADDLE_IMAGE_TAG` 选择官方标签构建基础镜像。
