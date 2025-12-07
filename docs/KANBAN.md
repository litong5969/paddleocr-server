# KANBAN

## Todo
- [ ] 技术探索：批量/大图性能评估方法与基准数据采集（p50/p95/p99）
- [ ] GUI-002：GUI 体验增强（复制按钮/历史记录/批量拖拽）
- [ ] Q1 里程碑：基础服务上线（Docker 镜像、/ocr API、缓存挂载指南）
- [ ] Q2 里程碑：监控/日志与认证接入（Prometheus/OpenTelemetry/Token）
- [ ] Q3 里程碑：批处理与队列化、版面/表格扩展、多语言模型切换
- [ ] Q4 里程碑：Helm/私有化一键部署、弹性伸缩与成本优化

## Doing
- MVP-001：/ocr API 最小实现切片与健康探针已落地（继续完善性能与观测）
- PERF-001：已实现 warmup、批处理与 Prometheus 指标；进行评估与调优
- DEP-001：K8s Kustomize 与 Helm Chart、GHCR CI 发布配置
 - GUI-001：轻量 Web GUI（/ui）单页 MVP 实现与集成

## Done
- [x] Temporary Bootstrap 完成（Integrity/Research/Planning OK，交接到 PM_BOOTSTRAP）
- [x] 研究检视：定位/用户/价值命题/竞品/MVP 范围/风险已补全
- [x] 基础设施配置：env 文件族、环境变量文档、docker compose 启动脚本；GPU/CPU 配置可调
- [x] 启动 PM 会话（session-001）：state-chain 建立与自检准备
- [x] /ocr API 规范与最小实现：`POST /ocr`、`/ocr/batch`、`/healthz`、`/readyz`、`/meta`，README 补充 Schema；GPU→CPU 自动回退与缓存挂载说明；Prometheus `/metrics` 与直方图/计数器
- [x] 安全与限制：单文件/批量大小限制、Content-Type 校验与 413/415 处理
- [x] 基准工具：`scripts/bench/bench_ocr.py` 并发基准脚本（简单 p50/p95/p99 输出）
- [x] 交付物：K8s manifests（ops/k8s/base,gpu）、Helm Chart（ops/helm/paddleocr-server）、GHCR 构建工作流
- [x] 设计文档：`docs/design/GUI_DESIGN.md`（方案与理由）
 - [x] GUI-001：复制按钮、历史记录（本地）、多文件拖拽与批处理调用 `/ocr/batch`
 - [x] GUI-002：导出按钮（.txt 下载）与 README 截图流程（SOP）
 - [x] GUI-003：元信息面板（/meta + /readyz）显示服务语言/版本/GPU/缓存/metrics/就绪状态
 - [x] PROXY-001：路径路由配置示例（K8s Ingress 与 Nginx），同端口同服务，避免跨域
 - [x] CI-001：GitHub Actions 轻量冒烟（pytest + Python 启动服务，验证 /healthz 与 /ui）
