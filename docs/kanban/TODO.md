# KANBAN（当前迭代）

## Todo
- [ ] README 增补 Demo 动图（可选）。

## In Progress
// 无

## Done
- [x] 端口与路径：GUI 与 API 共用 `5215`，GUI 暴露为 `/ui`。
- [x] `docker-compose.yml` 与 `.env.example`，挂载 `./web` 以便热更新。
- [x] 自检脚本 `make selfcheck`。
- [x] `make test` 与 `make perf-baseline` 入口脚本。
- [x] MVP GUI：拖拽/选择 → `/ocr`，整屏截图预览 → 确认后直送 OCR。
- [x] 发布 v0.2.0，并创建 GitHub Release。
