# 轻量 Web GUI 基线（Baseline v1）

本基线约束 paddleocr-server 内置 GUI 的实现范围、质量门槛与验收标准，确保与 Kernel 治理维度对齐。

## 目标与范围
- 单页原生 HTML/JS（不引入重量框架/打包器/CDN），作为 `/ui` 提供最小可用体验；`/` 重定向至 `/ui`。
- 仅覆盖“选择/拖拽图片 → 调用 `/ocr`/`/ocr/batch` → 展示文本与置信度”的核心路径。

## 治理对齐
- Architecture/Component：静态资源由 FastAPI `StaticFiles` 提供，复用现有进程；无新增进程与镜像。
- API Schema：严格复用现有 REST API；GUI 不新增后端接口。
- AI Coding：模型与推理路径不变；GUI 仅为调用层。
- Testing：提供最小 UI 可达性测试（FastAPI TestClient 检查 `/` 跳转 `/ui` 与关键文案）。
- Observability：沿用响应头 `X-Process-Time-ms` 与 Prometheus `/metrics`；GUI 显示服务端耗时与元信息。
- Performance：不引入大型依赖与打包；页面资源 < 50KB（文本）；首屏不阻塞。
- Security：仅在同源下工作；不请求外部脚本；前端限制 `image/*`；遵循后端上传大小限制与 413/415 处理。
- Reliability/SRE：就绪/存活探针不受 GUI 影响；GUI 失败不影响 API 可用性。
- DX：入口简洁，README 提供截图与 SOP，易于本地/内网体验。

## 验收清单（Checklist）
- [x] `/ui` 可用，`/` → `/ui` 重定向。
- [x] 单图与多图调用成功；错误提示清晰。
- [x] 复制/导出文本功能可用；最近 5 次历史可用、可清空。
- [x] 页面不依赖外网；不引入重量框架；资源体积小。
- [x] README 截图与 SOP；KANBAN/PM_LOG/ROADMAP 对齐。

## 版本与变更
- v1：初版（MVP + 复制/历史/导出 + 元信息显示）。
