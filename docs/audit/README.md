# Audit & Compliance (Kernel)

> 审计与自检规则，适用于任何新项目。

- 日志体系：raw log → summary → pm_state → PM_LOG。原始日志保存在 `ops/logs/pm/YYYY/MM/`，摘要在 `docs/summary/pm_sessions/`。
- Validator：`summary-validator` 必须保持绿灯；失败视为阻断，需先修复再继续交付。
- 自检：使用 `kernel/scripts/team-integrity-check/run_team_integrity_check.sh` 检查 agents/mcp/context7/文档完整性。
- ADR 记录：所有重要决策写入 `docs/adr/ADR-xxxx-title.md`，并在 Index/PM_LOG 备案。
- HOEP：高权限操作需脚本+双人审核（DEL 发起，OPQ 审核，Operator 执行），操作日志纳入审计。
