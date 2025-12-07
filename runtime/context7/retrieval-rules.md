# Retrieval Rules

- 优先按标签/路径过滤：governance、adr、standard、sop、runbook。
- 排序：recency 优先，其次语义相似度。
- 去偏置：限制单一来源命中文档数，确保多样性。
- 允许自定义知识库加载：在新项目中将自定义文档加入 embedding pipeline 即可。
