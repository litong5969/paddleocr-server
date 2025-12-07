#! Roadmap — paddleocr-server（GUI 联合端口 5215）

## 现在（MVP）
- 单页 GUI（`/ui`）：拖拽/选择图片 → 调用 `POST /ocr` → 显示文本与置信度。
- 截图按钮：HTTPS/localhost → PNG；内网 HTTP → 打印仅结果区域。
- 与 API 共端口：`5215`（容器 `5000`）。
- `docker-compose.yml` 支持挂载 `./web` 热更新。

## 下一步（Hardening）
- 自检 `make selfcheck`：健康检查 `/healthz`、OCR 冒烟（小图片）、GUI 资源 200 响应。
- README GUI 章节补充截图与使用说明。
-（可选）性能基线 `make perf-baseline` 脚本。

## 后续（可选）
- 历史记录更佳的预览与导出。
- 打印样式增加“仅识别文本”切换。
- 细节国际化与键盘无障碍。

