# 轻量 Web GUI — 设计与取舍

## 目标
- 在不增加镜像体积与冷启动成本的前提下，为内网/本地用户提供可直接在浏览器试用的 OCR 入口。
- 与 REST API 共存于同一容器，无需额外服务或代理。

## 方案与理由
- 技术路径：`FastAPI StaticFiles` 挂载静态资源（`/ui`），根路径 `/` 重定向到 `/ui`。
  - 无需新增依赖，复用 Starlette 能力；镜像体积与启动时间几乎不变。
  - 单页原生 HTML/JS（`web/ui/index.html`），避免引入 React/Vue 等重量框架。
- 交互范围：选择/拖拽图片 → `fetch('/ocr')` → 展示文本/置信度。
  - 只覆盖核心体验，不做状态管理、路由或组件库支持。
- 可观测性：复用服务端中间件耗时头 `X-Process-Time-ms`，UI 底部显示服务端耗时。

## 路由与部署
- 路由：
  - `/` → 302 到 `/ui`
  - `/ui` → 静态单页 GUI
  - 其余 API 保持不变：`/ocr`、`/ocr/batch`、`/healthz`、`/readyz`、`/meta`、`/metrics`
- 部署：
  - Dockerfile 新增 `COPY web ./web`，其余不变；K8s/Helm 无需变更。

## 后续演进（可选）
- 简易历史记录（LocalStorage）、复制按钮、拖拽多图批量（调用 `/ocr/batch`）。
- UI 主题切换与基础可达性（对比度、键盘可用性）。
