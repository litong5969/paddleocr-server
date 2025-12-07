# Engineering Standards (Kernel)

> 统一可执行的工程标准摘要（可在新项目直接落地）。

- Architecture：分层（route/controller/service/repo/middleware），无循环依赖，清晰边界。
- Components：前端组件分 base/layout/domain；命名/props/样式与别名规范；禁止跨层耦合。
- AI Coding：遵循 `kernel/docs/governance/PM_BOOTSTRAP.md` 中的轻量 AI 规则；生成代码需有测试与文档。
- API Schema：openapi.yaml 为 SSOT；生成类型/客户端；CI Gate 比对实现。
- Testing：多层测试（unit/integration/e2e）；Coverage 关注关键路径；Playwright/类似工具用于端到端。
- Observability：日志/metrics/trace 三件套；关键 SLI（可用性、延迟、错误率）纳入监控。
- Reliability & Performance：熔断/重试/超时/舱壁；容量/压测基线；性能回归检测。
- Security & SRE：威胁建模、鉴权/授权占位、配置/密钥策略；SLO/SLI/Error Budget。
- DX：脚手架、任务模板、Golden Path 示例，5 分钟定位写什么/写哪里。
