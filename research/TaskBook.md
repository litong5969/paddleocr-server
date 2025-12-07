# Research Inputs

## positioning
- 面向需要私有化/离线 OCR 的团队，提供轻量 Docker 化的 PaddleOCR HTTP 服务
- 主打“开箱即用 + GPU/CPU 双模支持”，作为自建识别链路的基础设施组件

## users
- 中小企业/数据标注团队：需要批量图片文本提取，且对数据合规/本地化有要求
- 内部工具/自动化脚本开发者：希望通过简单 API 将 OCR 能力嵌入工作流
- AI 平台团队：需要可扩展的推理服务基座，结合自身调度/网关

## value-proposition
- 一行 curl 即可使用的 REST API，降低接入成本
- 预置 PaddleOCR 模型缓存挂载位，减少冷启动下载时间
- 同一镜像支持 GPU 与 CPU，降低运维分发复杂度
- 自动化构建/推送到 DockerHub，便于持续交付

## competitors
- 云厂商 OCR API（阿里/腾讯/百度等）：功能齐全但依赖外网、计费不可控
- Tesseract 等开源 OCR：易部署但中英文效果及速度弱于 PaddleOCR
- 私有化推理框架（如 Triton + 自训模型）：灵活度高但集成成本高

## mvp-scope
- 端点：`POST /ocr`，表单文件字段 `file`
- 输出：文本行与逐行置信度
- 部署：Docker 镜像（latest、cuda12.6），支持 GPU/CPU 运行
- 配置：模型缓存挂载 `/root/.paddleocr`；基础日志

## risks
- 模型体积与首次下载时间影响冷启动
- GPU 依赖与驱动版本兼容风险
- 大图/批量请求可能导致内存占用攀升
- 缺少认证/限流，暴露在公网存在滥用风险

## vision
- 提供可插拔的模型管理与按需加载机制，缩短冷启动并提升多语言覆盖
- 集成认证、限流与监控（Prometheus/OpenTelemetry），适配生产网关
- 扩展多端点（表格/版面分析）、异步批处理与队列化调度
- 形成一键部署脚本/Helm Chart，覆盖私有云与边缘环境
