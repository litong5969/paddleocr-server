# 采集 Web GUI 截图（推荐流程）

> 目标：在 README 中展示真实界面截图，替换当前示意 SVG。

## 方式一：浏览器手工截图（最简单）
1) 启动服务：`docker compose --compatibility up -d --build`
2) 打开 `http://localhost:${HOST_PORT:-5213}/`，加载 `/ui`。
3) 使用系统截图工具截取主界面，保存到 `docs/summary/ui-screenshot.png`。
4) 更新 README 引用（如需将 PNG 替换为 PNG 链接）。

## 方式二：Chrome Headless 自动截图（脚本）
- 需要本机安装 Chrome/Chromium。
- 一键脚本：
  ```bash
  scripts/dev/capture_ui_screenshot.sh http://localhost:${HOST_PORT:-5213}/ docs/summary/ui-screenshot.png
  ```

完成后，将 README 中的 `ui-screenshot.svg` 切换为 `ui-screenshot.png` 即可。
