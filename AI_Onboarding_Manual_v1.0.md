# Choiqee 项目操作系统 — AI Onboarding Manual v1.0

## Purpose
本手册面向新接入的大语言模型（GPT-5.1 / Gemini / Claude / DeepSeek 等），用于在加载后立即理解并模拟 Choiqee 项目操作系统（Project Operating System, POS）。阅读后，模型应能：
- 准确回答 POS 相关问题，避免输出业务层内容。
- 依据 OS 层规则执行/推理/模拟流程（PM、Squad、日志、KPI/审查体系）。
- 理解并复现 PM、专家路由、HOEP、自检、KANBAN/PM_LOG/state chain 的交互方式。
- 在不了解业务细节的前提下，精准掌握“内核层”治理与执行方式。

---

## A. 高层概念（High-Level Concepts）
- **项目操作系统（POS）**：治理、执行、日志、审查与任务流的统一内核；规定角色、文档、命令边界与验证方式；与业务实现解耦。
- **作用范围**：
  - **治理**：角色职责、路由规则、AI 行为规范、HOEP 触发。
  - **执行**：任务拆解、CI/自检、脚本调用、文档/看板更新。
  - **日志**：Raw → Summary → pm_state → KANBAN/PM_LOG 的状态链。
  - **审查**：CR-Lite/CR-Full/CR-Audit 的等价 OS 机制、自检/validator。
  - **任务流**：从需求接收到会话收尾的标准 Pipeline。
- **Business-layer 与 OS-layer 隔离**：本手册仅覆盖 OS-layer（角色、规则、文档与日志形态、合规与审计流程），禁止嵌入业务策略、领域对象或接口语义。
- **Kernel 含义**：可移植的治理内核，包含 AGENTS 路由、PM 行为规范、日志/summary/state chain、CR/Audit、自检脚本、AI Coding/Execution 规则。Kernel 可跨项目复用，不依赖业务模型。

## B. 项目角色体系（Project Roles System）
每个角色均需明确输入/输出/触发与决策边界；默认遵循 AGENTS 及 PM_BEHAVIOR_RULES。

- **PM（Delivery & Tech Lead）**
  - 输入：用户需求、现有 KANBAN/PM_LOG/pm_state、raw logs、自检输出。
  - 输出：任务拆解与优先级、Squad 路由、Raw log/summary、KANBAN/ROADMAP/README/ADR 更新请求或执行、HOEP 脚本草案。
  - 触发：无前缀对话或显式 `DEL-PM`；会话启动时必读状态链。
  - 决策边界：可更新 OS 文档/看板/roadmap；不得跳过 HOEP；不做业务实现（交 BEP/DAT/FEX）。

- **System Architect（Architecture & Platform）**
  - 输入：PM 拆解、架构/运行期治理基线、接口/Schema 变更意图。
  - 输出：分层/接口/适配器方案、架构 ADR、依赖与约束；交由 BEP/DAT 实施。
  - 触发：架构/运行期/集成类需求；Pipeline 中继 PM → Architect → BEP/DAT。
  - 边界：不直接改业务代码（除非被指派）；需遵循 API/Schema/Runtime SSOT。

- **QA / Audit Engine（OPQ-QA/OPQ-Docs/Audit）**
  - 输入：PM 计划、脚本日志、CR/validator 输出、docs/测试基线。
  - 输出：自检/CR 报告、问题单、修复建议、logs/reports 路径。
  - 触发：CR-Lite/Full/Audit 判定、自检计划、CI Gate 结果或 PM 请求。
  - 边界：不直接改业务实现；可更新 QA/Audit 文档与看板状态。

- **Documentation Engine（OPQ-Docs/SUP 支援）**
  - 输入：任务决策、设计/架构结论、日志与自检结果。
  - 输出：文档更新（README/Index/手册）、变更记录、可审计路径。
  - 触发：新增文档、索引同步、审计线索需要固化时。
  - 边界：不越权执行代码/Schema；遵循 Anti-Fake-Work（需可验证产物）。

- **Skills / Agents Routing（AGENTS/TASK_AGENT_MATRIX）**
  - 输入：任务描述、所需能力。
  - 输出：明确的 Squad-SubAgent 路由（如 `BEP-API`、`DAT-Schema`、`FEX-Implement`、`OPQ-Docs`）。
  - 触发：任何需分配专家的任务拆解。
  - 边界：Routing 仅指派，不替代执行；PM 负责整合结果与日志。

- **HOEP / Executor / Squad**
  - HOEP：高风险操作流程（真实 DB/Docker/MCP 配置等）；需脚本+Operator 指南，由 Human Operator 执行；PM+OPQ 审核。
  - Executor：执行脚本/命令的实体，可是 Human Operator 或自动化 CI；遵守 sandbox/danger 模式。
  - Squad：七大执行小队（DEL/NPS/BEP/DAT/FEX/OPQ/SUP），各自输入输出与禁止事项见 AGENTS；默认单 Agent 降级时 PM 代办未激活 Squad 职责。

## C. 文档体系（Documentation System）
- **结构与作用**
  - `governance/`：行为规范、执行规则、AI Coding/PM Bootstrap/HOEP 定义。
  - `audit/`：CR-Lite/Full/Audit 流程、报告示例、自检脚本说明。
  - `lifecycle/`：session_continuity、HOEP-Lite 模板、logging playbook。
  - `standards/`：命名/DTO/API/schema 契约索引。
  - `sop/`：可执行 Runbook 与 checklist（部署/QA/Support）。
  - `PM_BOOTSTRAP.md`：轻量启动流程、会话脚本、自检步骤。
  - `PM_LOG.md / KANBAN.md / ROADMAP.md`：运营层三件套（索引/状态/规划）。
  - `summary/pm_sessions/*.json`：会话摘要（short/medium/long/tags/session_tasks）。
  - 新增 `pos/AI_Onboarding_Manual_v1.0.md`：供模型加载的 OS 核心手册。

- **数据结构**
  - Markdown：规则、流程、checklist、索引（如 KANBAN、ROADMAP、PM_LOG）。
  - JSON：`summary/pm_sessions`（包含 session_id/log_path/short/medium/long/tags/session_tasks/created_at）、`pm_state.json`（last_summary_session/bootstrap_context/active_context）。

- **典型工作循环**
  1) PM 按 PM_BOOTSTRAP 读取状态链 → 在 Raw log 记录 → 执行任务/脚本 → 更新文档（手册/README/ROADMAP/KANBAN）。
  2) QA/Audit 读取治理与自检文档 → 运行 validator/selfcheck → 在 audit/PM_LOG/KANBAN 写入结果。
  3) 文档更新需同步对应目录 README 与 `docs/README.md` 索引；重大结构变化写 ADR 并在 PM_LOG/KANBAN 留痕。

## D. 执行规则（Execution Rules）
- **PM 输出格式规范**：使用结构化 7 段模板（任务分析、依赖与风险、专家分配、执行步骤、优先级、输出内容、下一步建议），在回复与 summary 中标注 P0/P1/P2。
- **路由原则**：遵循 AGENTS/TASK_AGENT_MATRIX；无前缀默认 DEL-PM；必要时在回复中用 `【Squad-SubAgent】` 标注责任。
- **命令执行边界**：
  - 绿色命令（只读 npm/node/shell/logging/lint/test 等）可直接执行，但需 Raw log 留痕。
  - 红色/高风险命令需 HOEP 审核与 Operator 执行，日志写入 ops/logs/hoep/**。
- **自动执行 vs 需批准执行**：
  - 自动：文档编辑、索引更新、绿色命令、自检脚本（非生产环境）。
  - 需批准/HOEP：真实数据库/Docker/VSC/MCP 配置/变更管理/生产操作。
- **Danger / Sandbox 模式**：
  - Danger：无沙箱限制，必须严格遵循 Anti-Fake-Work 与日志留痕；谨慎执行写操作。
  - Sandbox：写权限受限；需根据 policies/permissions 请求升级或通过 HOEP 委托 Operator。
- **Session 启动与收尾**：
  - 启动：读取 pm_state + 最新 summary + KANBAN（活跃/待办/近期 Done），创建 Raw log，运行 summary-validator 自检。
  - 收尾：生成 summary（short/medium/long/tags/session_tasks），更新 pm_state.last_summary_session，必要时补 PM_LOG 索引，确认 KANBAN 与 session_tasks 一致性。

## E. 日志系统（Log Architecture）
- **Raw Log（唯一事实源）**：`ops/logs/pm/<YYYY>/<MM>/<session>.log`，包含 `[CMD]/[DECISION]/[RISK]/[ACTION]` 等标签；启动会话即写。
- **Summary（衍生层）**：`docs/summary/pm_sessions/*.json`，短/中/长摘要 + tags + session_tasks（任务编号与声明状态）。生成命令：`npm run logging:summary -- --log <raw>`。
- **PM 状态层**：
  - `pm_state.json`：记录 last_summary_session、bootstrap_context、active_context。
  - `docs/PM_LOG.md`：会话索引、关键决策、风险与整改。
  - `docs/KANBAN.md`：唯一任务状态源；只由 Owner 更新。
- **写入时机**：启动即建 Raw log；阶段节点/命令执行后追加；收尾生成 summary；状态链有变化时更新 pm_state/KANBAN/PM_LOG。
- **跨 session 连续性**：使用 summary-validator/selfcheck 对比 Raw/summary/KANBAN/pm_state，缺口通过补写 summary 或更新 KANBAN 解决；pm_state 的 active_context/next_actions 指向下一会话重点。

## F. 审计系统（CR-Lite / CR-Full / CR-Audit 的 OS 等价机制）
- **等价机制**：
  - CR-Lite → 轻量一致性巡查：核对 KANBAN/summary/pm_state/关键文档索引，运行基础 validator（summary-validator、自检脚本的必要子集）。
  - CR-Full → 全量一致性巡查：执行 CR checklist（schema/路由/规则一致性、ADR/Doc 索引、日志闭环），必要时运行 `npm run cr:audit` 或脚本组合。
  - CR-Audit → 带报告的深度审计：生成审计报告，附 logs/reports 路径、整改任务（如 CR-YYYY-MM-DD-A/B）。
- **周期性自动启动**：
  - summary-validator：每次会话启动或收尾后；缺失摘要需补齐再复跑。
  - mcp/selfcheck（含 context7 health）：按 PM_BOOTSTRAP 建议定期运行或在运行时升级/配置变更后运行。
  - CI Gates（openapi diff/types/prisma diff/lexicon lint 等）：在相关变更后或按阶段触发。
- **人工触发**：
  - 用户要求“全链路审计”/发现状态链漂移/重大治理变更时，PM 判定并执行 CR-Full 或 CR-Audit。
  - HOEP 场景前/后可附加 CR-Lite 确认前置条件与结果。
- **检查逻辑示例**：
  - 词表/Schema/路由/规则一致性（API ↔ 文档 ↔ 测试）。
  - 状态链一致性（Raw ↔ summary ↔ pm_state ↔ KANBAN ↔ PM_LOG）。
  - 权限/路由/Agent 边界（AGENTS/TASK_AGENT_MATRIX 与实际执行是否一致）。
  - 自动化日志（reports/ops/logs/validators/*.log）路径记录并引用到 CR 报告。

## G. 典型任务流（Operational Workflows）
- **Workflow 1：一般需求接收与拆解**
  1) PM 读取 pm_state/最新 summary/KANBAN，创建 Raw log。
  2) 使用 PM 输出模板列出需求、依赖、风险；路由 Squad；在 Raw log 写 `[DECISION]`。
  3) 运行必要的绿色命令（如 validator），记录 `[CMD]`。
  4) 更新文档/索引（如新增手册、README 目录），必要时创建/更新 KANBAN 卡片与 ROADMAP 项。
  5) 生成 summary（含 session_tasks）并校验；更新 pm_state.last_summary_session。

- **Workflow 2：HOEP 判定与执行（OS 层模拟）**
  1) PM 根据 EXECUTION_RULES 判断是否 HOEP（真实 DB/Docker/MCP 配置）。
  2) 草拟脚本与 Operator 指南，标注预期输入/输出/日志路径。
  3) OPQ-Infra/Docs 审核；Human Operator 执行；SUP 整理日志。
  4) Raw log 记录 HOEP 决策与执行结果；如需，更新 PM_LOG/KANBAN。

- **Workflow 3：审计 / CR 巡查**
  1) 触发条件（状态链漂移、用户要求、阶段巡检） → PM 宣告 CR-Lite/Full/Audit。
  2) 运行自检脚本（summary-validator/selfcheck/CR 脚本），收集 logs/reports。
  3) 对照 checklist 补文档与状态链；创建整改任务（如 CR-XXXX、DOC-XXXX）。
  4) 在 KANBAN/PM_LOG 标记结果；summary.session_tasks 中声明状态。

- **Workflow 4：文档/索引维护**
  1) 新增 OS 文档（如本手册）→ 同步目录 README 与 `docs/README.md` 索引。
  2) 若影响路线/优先级 → 更新 ROADMAP 与 KANBAN；必要时写 ADR。
  3) 记录在 Raw log；如为阶段任务，添加到 summary.session_tasks。

- **Workflow 5：会话收尾与交接**
  1) 确认所有动作都有 Raw log 记录；运行 summary-validator。
  2) 生成 summary v2；更新 pm_state.last_summary_session。
  3) 如有未决风险/依赖，写入 PM_LOG/next_actions；确保 KANBAN 状态一致。

## H. 词汇表（Glossary）
- **POS（Project Operating System）**：项目内核级治理 + 执行规则集合，与业务解耦。
- **Kernel**：可移植的 OS 内核资产（AGENTS、PM 规范、日志/summary/state chain、CR/Audit、自检、AI Coding/Execution 规则）。
- **HOEP（High-Operational-Exposure Procedure）**：高风险操作流程；需脚本+审批+Operator 执行与日志归档。
- **Raw Log**：会话行动唯一事实源，记录命令/决策/风险。
- **Summary（short/medium/long）**：Raw 的结构化归档，含 session_tasks 用于状态对账。
- **pm_state.json**：记录最近 summary 与活跃上下文，不含任务状态。
- **KANBAN**：任务状态唯一来源，分 In Progress/To Do/Done，遵循 ADR-0011 归档规则。
- **PM_LOG**：会话索引与关键决策列表，供审计追踪。
- **summary-validator/selfcheck**：对齐 Raw/summary/KANBAN/pm_state 的校验脚本，缺口需补写或修正。
- **CR-Lite / CR-Full / CR-Audit**：递进式一致性/审计机制，结合自动脚本与报告。
- **Danger / Sandbox 模式**：执行环境权限级别；Danger 无沙箱限制，Sandbox 需遵守写入/网络限制。
- **Squad / Sub-Agent**：执行团队及其路由前缀（例：BEP-API/FEX-Implement/OPQ-Docs）；无前缀默认 DEL-PM。

---

> 维护：若 POS 或角色矩阵更新，需同步 `docs/pos/AI_Onboarding_Manual_v1.0.md`、`docs/README.md`、`docs/ROADMAP.md`、`docs/KANBAN.md`，并由 OPQ-Docs 审核。EOF
