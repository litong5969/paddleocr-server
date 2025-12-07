# Embedding Rules

- 使用统一 embedding schema：`{title, body, tags, source, timestamp}`。
- 默认分段：800-1200 字符，重叠 100-150。
- 过滤：去除敏感/凭据信息；忽略 node_modules、dist、logs 等产物。
- 更新策略：变更 doc/ADR/standard 时触发重嵌入。
