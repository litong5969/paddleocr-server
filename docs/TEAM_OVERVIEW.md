# Team Overview (Kernel)

> 本文件提供可移植的团队结构与职责分工，无业务绑定。

## Squad 职责摘要
- **DEL – Delivery & Coordination**：需求澄清、Roadmap/KANBAN 维护、HOEP 调度、KPI 追踪。
- **NPS – Narrative & Prompt**：叙事结构、Prompt/LLM 模板、JSON Schema。
- **BEP – Backend & Platform**：架构分层、API/中间件、Provider/脚手架。
- **DAT – Data & Intelligence**：Schema 设计、迁移/回填、分析与推荐基线。
- **FEX – Frontend Experience**：IA、组件/状态管理、Playwright/E2E。
- **OPQ – Ops & Quality**：QA、自检、文档、合规/风控、监控、商业化。
- **SUP – Support & Assistant**：跨 Squad 支援、提示词整理、日志协调。
- **SA – Strategic Advisor**：中长期路线顾问（只读）。

## 汇报与决策
- PM 负责日常决策与验收；重大治理/架构调整需 ADR 记录并由 OPQ-Docs 复核。
- HOEP（高权限执行流程）需 DEL/OPQ 审核，Human Operator 执行。

## 文档 SSOT
- 路由与角色：`kernel/AGENTS.md`
- 任务矩阵：`kernel/docs/TASK_AGENT_MATRIX.md`
- PM 启动流程：`kernel/docs/governance/PM_BOOTSTRAP.md`
- 自检/审计：`kernel/docs/audit/`、`kernel/runtime` 内核配置
