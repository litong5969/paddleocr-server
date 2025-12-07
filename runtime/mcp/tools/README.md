# MCP Tools (Kernel)

可根据项目需要挂载具体工具；默认建议：
- `fs`：受限文件读/写
- `shell`：只读 shell，危险命令需审批
- `git`：status/log 只读
- `tests`：运行测试套件
- `summary-validator`：校验 summary/pm_state/KANBAN 结构

安装时将实际工具配置指向本目录或上层 registry/policies。保持与 `registry.yml` / `policies.yml` 前缀一致。
