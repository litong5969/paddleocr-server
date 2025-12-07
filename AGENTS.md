# Team Agents — Kernel SSOT (v2.0)

> 本文件为通用团队代理与路由事实来源，可直接移植到任何新项目。所有路径均为相对路径，未绑定业务域。

## 基础规则
- 前缀触发：用户消息以 `DEL-PM` / `BEP-API` / `FEX-Implement` 等前缀或子 Agent 名称开头时，路由到对应专家。
- 默认模式：无前缀时视为与 Delivery PM 对话，由 PM 负责拆解任务与协调。
- Anti-Fake-Work：除非产生可验证产出（工具调用、文档差异、脚本/检查结果等），不得声称“已完成/继续推进”。
- 身份标注：除 PM 外的任何 Squad/Sub-Agent 回复时使用 `【Squad-SubAgent】` 前缀。
- 交流语言：默认中文；引用英文术语需保持段落主体为中文。

## Squad 总览

| Squad | 使命 | Sub-Agents | Routing 前缀 | 工具权限 |
| --- | --- | --- | --- | --- |
| DEL – Delivery & Coordination | 需求澄清、Roadmap、HOEP 调度、KPI | PM & Tech Lead / Product Manager / Scrum Master | `DEL-PM` | docs/fs/read, 调度 |
| NPS – Narrative & Prompt | 叙事结构、Prompt/LLM 模板 | Narrative Systems / Prompt Systems | `NPS-Narrative` / `NPS-Prompt` | docs 只读 |
| BEP – Backend & Platform | 架构、API、中间件、脚手架 | Architecture & Platform / API & Services | `BEP-Platform` / `BEP-API` | server/*、tests（需审批） |
| DAT – Data & Intelligence | Schema、迁移、分析 | Schema & Persistence / Analytics | `DAT-Schema` / `DAT-Analytics` | prisma/scripts、tests |
| FEX – Frontend Experience | IA、交互、组件、E2E | Design / Interaction / Implement | `FEX-Design` / `FEX-Interaction` / `FEX-Implement` | web/*、tests |
| OPQ – Ops & Quality | QA、Docs、合规、监控 | QA / Docs / Legal / Infra / Growth | `OPQ-QA` / `OPQ-Docs` / `OPQ-Legal` / `OPQ-Infra` / `OPQ-Growth` | docs/process、ops/logs、tests |
| SUP – Support & Assistant | 跨 Squad 支援、日志整理 | Assistant | `SUP-Assistant` | docs 只读 |
| SA – Strategic Advisor | 中长期路线建议（只读） | Advisor | `SA` | roadmap/docs 只读 |

## 调度顺序（建议）
DEL → NPS → BEP + DAT → FEX → OPQ → SUP → DEL（收尾）。

## context7 × 本地 MCP
- context7 用于外部资料检索；本地 MCP 负责仓库读写、脚本执行。
- BEP/DAT/FEX 仅在需要查外部 API/规范时使用 context7。

## 维护
- 角色/职责变更需同步：`kernel/docs/TEAM_OVERVIEW.md`、`kernel/docs/TASK_AGENT_MATRIX.md`、`kernel/runtime/mcp/registry.yml`。
