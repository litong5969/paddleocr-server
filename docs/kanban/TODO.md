# KANBAN（当前迭代）

## Todo
- [ ] README 增补 HTTPS/TLS 开启与整屏截图说明（已基础覆盖，补图待确认）。

## In Progress
- [ ] README 截图与视频 Demo（可选）。

## Done
- [x] 端口与路径：GUI 与 API 共用 `5215`，GUI 暴露为 `/ui`。
- [x] `docker-compose.yml` 与 `.env.example`，挂载 `./web` 以便热更新。
- [x] 自检脚本 `make selfcheck`。
- [x] `make test` 与 `make perf-baseline` 入口脚本。
- [x] MVP GUI：拖拽/选择 → `/ocr`，整屏截图预览 → 确认后直送 OCR。
