# Delivery Lifecycle (Kernel)

> 轻量工作流，封顶治理基线（无业务绑定）。

1. Intake：需求收集 → DEL-PM 快速澄清 → Feature Priority Framework 排序。
2. Design：参考架构/组件/AI Coding/Schema/Testing/Observability/Security/SRE/DX 规范；必要时起 ADR。
3. Build：使用脚手架与模板，保持目录/命名一致；CI Gates（lint/test/schema diff/validator）必须通过。
4. Validate：summary-validator/selfcheck；QA 验收，必要监控/日志检查。
5. Document：更新 KANBAN、PM_LOG、Documentation Index、summary、pm_state；记录 ADR。
6. Release：按 Change Management 与 Runbook 流程交付；必要时触发 HOEP。
7. Maintain：处于 Maintenance Mode，不开启新治理 Phase，仅修正漂移与索引。
