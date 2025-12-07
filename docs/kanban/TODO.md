# KANBAN（当前迭代）

## Todo
- [ ] README 增加 GUI 章节与截图占位（`docs/summary/ui-screenshot.png`）。
- [ ] 自检脚本 `make selfcheck`：/healthz、/ocr 冒烟、/ui 资源检查。
- [ ] （可选）基准脚本 `make perf-baseline`（本地 SSOT）。

## In Progress
- [ ] MVP GUI：单页、拖拽/选择、调用 `POST /ocr`、显示文本与置信度、截图按钮（已提交初版）。

## Done
- [x] 端口与路径：GUI 与 API 共用 `5215`，GUI 暴露为 `/ui`。
- [x] `docker-compose.yml` 与 `.env.example`，挂载 `./web` 以便热更新。

