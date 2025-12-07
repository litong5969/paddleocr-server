# 本地 Gate（Dev/Dev Mirror SSOT）

> 原则：CI 仅作为分支保护 Gate；唯一事实源为本地可重复命令。以下命令在 Dev/Dev Mirror 环境通过，即视为 CI 可通过。

## 命令总览
- 自检（结构/文档/端点冒烟/容器内测试）
  ```bash
  make selfcheck
  # 等价：scripts/dev/selfcheck.sh
  ```
- 单元测试（容器内，FakeOCR）
  ```bash
  make test
  # 等价：scripts/dev/run_tests.sh
  ```
- 性能基线（并发 1/4/8，结果写入 docs/summary/bench-<date>.md）
  ```bash
  make perf-baseline
  # 等价：scripts/dev/perf_baseline.sh
  ```

## 说明
- 自检包含：team-integrity-check、若服务已运行则对 /healthz /ui /meta 的冒烟校验，以及容器内 pytest。
- 性能脚本默认目标：`http://localhost:${HOST_PORT:-5215}/ocr`，可通过环境变量 URL/IMG/REQS/CONC_LIST/OUT 覆盖。
- 如需在 CI 重用，可直接调用这些脚本；无需读取 Actions 输出作为事实源。
