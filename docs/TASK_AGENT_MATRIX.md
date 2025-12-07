# Task-Agent Matrix (Kernel)

> 任务类型与负责 Squad/Agent 对照表，可用于新项目的快速路由。

| 任务类型 | Owner | 协作 | 备注 |
| --- | --- | --- | --- |
| 需求澄清 / KANBAN 更新 / PM_LOG | DEL-PM | OPQ-Docs | 默认入口 |
| Prompt/LLM 模板 / 叙事结构 | NPS-Prompt / NPS-Narrative | DEL-PM | 不改数据库/前端 |
| 架构设计 / API 路由 / 中间件 | BEP-Platform / BEP-API | DEL-PM / OPQ-Infra | Schema 变更交 DAT |
| Schema 设计 / 迁移 / 回填 | DAT-Schema | BEP-API / OPQ-QA | 需要测试覆盖 |
| 分析/推荐/指标 | DAT-Analytics | BEP-API / OPQ-Infra | 与 Observability 对齐 |
| 前端 IA/组件/状态/E2E | FEX-Design / FEX-Interaction / FEX-Implement | BEP-API / OPQ-QA | 遵循组件治理 |
| QA / 文档 / 合规 / 监控 | OPQ-QA / OPQ-Docs / OPQ-Legal / OPQ-Infra | 全体 | summary-validator/selfcheck |
| 支援 / 日志整理 / 术语 | SUP-Assistant | DEL-PM / OPQ-Docs | 无高风险命令 |
| 战略顾问 | SA | DEL-PM | 只读、不可执行 |

## 升级与审批
- 高权限操作（真实 DB、生产基础设施）必须走 HOEP，脚本由 DEL 起草、OPQ 审核、Human Operator 执行。
- 超出矩阵职责的需求，PM 需在 KANBAN/PM_LOG 说明例外原因。
