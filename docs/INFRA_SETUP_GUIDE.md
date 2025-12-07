# **PutBack 基础设施配置指南（Infrastructure Setup Guide）**

> **本文档用于指导 PM 完成 PutBack 项目的基础设施（Postgres / Redis / Env）初始化与规范化。**
>  目标是确保 PutBack 能在 Unraid 环境中顺利运行，并具备可扩展性、稳定性和清晰的环境隔离。

------

# **1. 总体目标**

PutBack 作为独立项目，需要具备：

- 独立且稳定的数据库（Postgres）
- 可靠的缓存 / 会话系统（Redis，可选但推荐）
- 完整、可扩展的 `.env` 变量结构（基于 `.env.template`）
- 清晰的容器命名与端口管理，不与现有服务冲突
- dev / prod 环境按照 database / Redis DB index 隔离

------

# **2. 数据库规划（Postgres）**

PutBack 需要一个独立且规范化的 Postgres 实例。

## **2.1 创建 Postgres 容器**

请创建一个新的 Postgres 容器，命名为：

```
shared-postgres
```

> PutBack 不需要独占实例，未来若有其他小型服务，也可以使用该实例。
>  该实例不与主产品共享资源，避免资源竞争与迁移风险。

### 推荐配置：

- **镜像**

  ```
  postgres:16-alpine
  ```

  （如未来加入向量嵌入，可改用 `pgvector/pgvector:pg16`）

- **宿主机端口**

  ```
  5442
  ```

  ※ 在创建前请检查端口是否占用（见第 6 节）

- **卷挂载路径**

  ```
  /mnt/user/appdata/shared-db/postgres
  ```

------

## **2.2 在实例内创建 PutBack 的数据库**

Postgres 实例中应包含两个 database：

```
putback_prod
putback_dev
```

将 `.env` / `.env.dev` 中的 `DATABASE_URL` 指向以上库。

------

# **3. Redis 配置（可选，但推荐）**

Redis 用于：

- 登录会话（session）
- 速率限制（rate limit）
- 缓存
- 异步任务队列（未来可能添加）

建议新建一个 Redis 实例，命名为：

```
shared-redis
```

### 推荐配置：

- **镜像：**

  ```
  redis:7-alpine
  ```

- **端口：**

  ```
  6382
  ```

- **卷挂载路径：**

  ```
  /mnt/user/appdata/shared-db/redis
  ```

### Redis DB index 规划：

| 环境 | Redis DB index |
| ---- | -------------- |
| prod | 0              |
| dev  | 1              |

------

# **4. 环境变量配置（基于 `.env.template`）**

项目根目录已提供 `.env.template`，该文件是 PutBack 的环境变量唯一事实源（SSOT）。

请执行以下工作：

## **4.1 对齐所有 `.env\*` 文件**

需要更新的文件：

- `.env`
- `.env.dev`
- `.env.preprod`（如有）
- `.env.example`
- `.env.sample`

### 对齐规则：

1. `.env.template` 中的字段全部保留。
2. 若 `.env` 中已有但模板未包含字段，则将它们加入模板（不得删除）。
3. 字段命名如有不一致，应统一为模板规范。
4. `.env.example` / `.env.sample` 必须与 `.env.template` 字段完全一致（可留空）。
5. `.env` / `.env.dev` 填写实际值。

------

## **4.2 变量兼容迁移**

如果发现不同变量名指代相同概念（如两个 BASE_URL），需要：

1. 建立“旧名 → 新名”对照表
2. 更新代码的变量读取逻辑，优先读取新变量，兼容旧变量
3. 在日志中提示旧变量已废弃（deprecation warning）

示例：

```
const API_BASE =
  process.env.API_BASE_URL ??
  process.env.VITE_API_BASE ??  // deprecated
  'http://localhost:4000';
```

------

# **5. 容器命名规范**

为保证部署清晰，请遵循以下命名：

| 类型          | 容器名                                  |
| ------------- | --------------------------------------- |
| Postgres 实例 | `shared-postgres`                       |
| Redis 实例    | `shared-redis`                          |
| 后端服务      | `putback-api`（示例，可按项目结构调整） |
| 前端服务      | `putback-web`（示例）                   |

------

# **6. 启动前检查（必须执行）**

在创建容器前，请确认端口未被占用：

```
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

以及：

```
sudo lsof -i -P -n | grep LISTEN
```

确认以下端口可用：

- `5442`（Postgres）
- `6382`（Redis）

如冲突，请选择相邻端口，并在变更说明中记录。

------

# **7. 输出结果要求**

完成配置后，请提交：

1. 新建或更新后的 Postgres / Redis 容器配置（docker-compose 片段）

2. 更新后的 `.env` / `.env.dev` / `.env.example`

3. 变量对照表（如有重命名）

4. 数据库连接测试结果

   ```
   psql -h localhost -p 5442 -U postgres -d putback_prod
   ```

5. 若使用 Redis，测试连接：

   ```
   redis-cli -p 6382 ping
   ```

------

# **8. 文档维护**

请将所有环境变量字段与含义整理至：

```
docs/ENVIRONMENT_VARIABLES.md
```

并保持与 `.env.template` 同步。

------

# **结语**

完成本文档中的初始化步骤后，PutBack 项目将具备：

- 清晰可维护的基础设施结构
- 安全可靠的环境隔离
- 可扩展的部署方案
- 与未来 AI/队列/SSO 功能完全兼容的配置体系

请在开始实现前确认配置步骤均已完成。