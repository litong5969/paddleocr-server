# SOP — Operating Procedures (Kernel)

- **HOEP（高权限执行流程）**：DEL 起草脚本，OPQ 审核，Human Operator 执行；全程日志；禁止自动绕过审批。
- **Change Management**：小步发布、可回滚；feature flag 占位；记录变更与审批链。
- **Incident Response**：分级 P1/P2/P3；检测→确认→缓解→修复→回溯；timeline 模板统一。
- **Runbook**：维护/故障/回滚/性能排查步骤模板；至少保留一条演练记录。
- **Audit Trail**：PM_LOG、ADR、summary、ops/logs/* 应可回溯；归档与索引更新。
- **Maintenance Mode**：默认不引入新治理 Phase；仅修复漂移、补文档索引、保持 validator 绿灯。
