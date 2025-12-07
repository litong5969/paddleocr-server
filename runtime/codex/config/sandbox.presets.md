# Sandbox Presets

- **standard-isolation**：workspace-write、network enabled、approval on-request。用于日常开发，阻断高危命令。
- **danger-full-access**：danger-full-access、network enabled、approval on-request。仅限调试或特批场景，需在 HOEP 下使用。

加载方式：在 Codex CLI 配置中选择对应 preset，并确保使用 `codex.config.json` 指定的 registry/policies。
