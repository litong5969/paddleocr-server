# PM Closeout — 会话收尾规范（paddleocr-server）

目的：在每次迭代结束时固化产出、冻结范围、同步路线与看板，并产生可验证的交付记录。

标准步骤（SSOT）
1. 冻结范围与版本
   - 更新 CHANGELOG 与 README 要点
   - 打标签（语义或里程碑）：`vX.Y.Z`
   - 创建 GitHub Release（附发布说明/链接）
2. 固化可验证产出
   - 产出路径清单（代码/脚本/文档/截图）
   - 本地 Gates（可在 Dev/Dev Mirror 执行）：`make selfcheck` / `make test` / `make perf-baseline`
3. 同步路线与看板
   - Roadmap 标记“已交付/下一步”
   - KANBAN 移动条目至 Done/Backlog
4. 会话归档
   - 写入 `docs/summary/pm_sessions/closeout-<date>.md`（含版本、提交、Release 链接、产出、后续）

当前迭代（示例：v0.2.0）
- 版本：v0.2.0（轻量 Web GUI + 整屏截图→确认→OCR）
- 端口：5215（API+GUI 共端口），GUI 路径 `/ui`，API `/ocr`。
- TLS：同端口可选（`SSL_CERTFILE` / `SSL_KEYFILE`）。
- Gates 原则：CI 仅 gate，本地 `make` 命令为唯一事实源（无需读取远端 Actions 输出）。

