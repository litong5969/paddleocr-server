# Integrations

- **MCP**：使用 `registry.yml` / `policies.yml`；工具目录 `kernel/runtime/mcp/tools/`。保持与 Codex CLI sandbox preset 一致。
- **context7**：providers 定义见 `kernel/runtime/context7/providers.json`；embedding / retrieval 规则参考同目录说明。
- **CI Gates**：建议在新项目接入 lint/test/schema-diff/summary-validator，自检脚本可复用 `kernel/scripts/team-integrity-check`.
- **Logging**：raw log → summary → pm_state / PM_LOG；可在 ops/logs 下落盘，确保审计路径可配置。
