# PM Bootstrap — 开启会话进程（paddleocr-server）

时间：2025-12-08

目标：将“轻量级 Web GUI（单页，集成在同一镜像，走 /ui）”纳入基线与路线图，并交付最小可用版本（MVP）。

决策与约束
- 与 REST API 共端口（HOST_PORT=5215），路径共存：/ocr 与 /ui。
- 内网使用，不启用认证与限流；Metrics 默认关闭。
- 前端不引入重量级框架，纯 HTML/CSS/JS。

立即产出（Anti-Fake-Work 可验证）
- 新增 `web/ui/index.html`，实现拖拽/选择图片，调用 POST /ocr，展示文本与置信度；加入“截图”按钮：
  - HTTPS/localhost → getDisplayMedia 抓取活动标签页并下载 PNG。
  - 其它（如内网 HTTP）→ 打印仅“识别结果”区域，便于另存为 PDF。
- 新增 `.env.example`（`HOST_PORT=5215`）与 `docker-compose.yml`（挂载 `./web` 到容器 `/app/web`）。

后续动作（按 KANBAN 跟踪）
1) 文档完善：README 增加 GUI 说明与截图占位。
2) 自检脚本：加入 `make selfcheck`（端点冒烟 + GUI 静态资源检查）。
3) 性能基线：提供 `make perf-baseline`（可选）。
4) CI 只作 Gate，本地 `make` 命令为唯一事实源（SSOT）。

