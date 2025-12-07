# Temporary Bootstrap

## 0. Purpose
本引导器仅在迁移/新项目启动时运行一次，确保在加载 Kernel 前完成团队完整性、研究输入与规划文件生成。

## 1. Team Integrity Check
- 运行：`bash kernel/scripts/team-integrity-check/run_team_integrity_check.sh`
- 阻断条件：任一检查失败（agents/registry/policies/context7/PM_BOOTSTRAP/lifecycle/日志目录），需修复后再继续。

## 2. Product Strategy Check
- 使用 `kernel/research/*.md` 填写：positioning、users、value-proposition、competitors、mvp-scope、risks、vision。
- 未完成或缺失内容时阻断启动。

## 3. Generate Planning Files
- 创建/覆盖以下结构（示例任务：启动、研究检视、MVP 范围、技术探索、Q1–Q4 关键节点）：  
  - `docs/KANBAN.md`  
  - `docs/ROADMAP.md`  
  - `docs/PM_LOG.md`  
  - `docs/summary/`  
  - `docs/governance/`  
  - `docs/audit/`  
  - `docs/lifecycle/`  
  - `docs/standards/`  
  - `docs/sop/`
- 填入基础卡片：启动任务、研究检视、MVP 确认、技术探索、各季度里程碑。

## 4. Handover Logic
- 当 Integrity=OK 且 Research=OK 且 Planning=OK：  
  - 在 PM_LOG 写入：`Integrity: OK; Research: OK; Planning: OK; Ready to load PM_BOOTSTRAP`  
  - 按`INFRA_SETUP_GUIDE.md`初始化基础设施
  - 切换到 `kernel/docs/governance/PM_BOOTSTRAP.md` 进入常态工作流。

## 5. Disable & Archive
- Temporary Bootstrap 仅运行一次。完成交接后：  
  - 在 PM_LOG 记录“temporary_bootstrap completed and archived”。  
  - 在 KANBAN Done 区标记“Temporary Bootstrap 完成”。  
  - 后续会话直接使用 PM_BOOTSTRAP，不再调用本文件。
