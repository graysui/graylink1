# 数据库配置说明

## 配置选项

### 基础配置
```yaml
database:
  url: sqlite+aiosqlite:///data/graylink.db  # 数据库连接 URL
  echo: false                                # 是否打印 SQL 语句
```

### 连接池配置
```yaml
database:
  pool_size: 20          # 连接池大小
  max_overflow: 10       # 最大溢出连接数
  pool_timeout: 30       # 连接池超时时间（秒）
  pool_recycle: 3600    # 连接回收时间（秒）
```

### 性能配置
```yaml
database:
  batch_size: 1000      # 批处理大小
```

## 环境变量

可以通过环境变量覆盖配置文件中的设置：

```bash
# 数据库 URL
GRAYLINK_DATABASE__URL=postgresql+asyncpg://user:pass@localhost/db

# 连接池设置
GRAYLINK_DATABASE__POOL_SIZE=30
GRAYLINK_DATABASE__MAX_OVERFLOW=15
GRAYLINK_DATABASE__POOL_TIMEOUT=60
GRAYLINK_DATABASE__POOL_RECYCLE=7200

# 其他设置
GRAYLINK_DATABASE__ECHO=true
GRAYLINK_DATABASE__BATCH_SIZE=2000
```

## 配置说明

### 数据库 URL
- **SQLite**: `sqlite+aiosqlite:///data/graylink.db`
- **PostgreSQL**: `postgresql+asyncpg://user:pass@host/dbname`
- **MySQL**: `mysql+aiomysql://user:pass@host/dbname`

### 连接池参数

1. **pool_size**
   - 默认值：20
   - 说明：连接池保持的连接数
   - 建议：根据并发需求调整，通常设置为 CPU 核心数的 2-4 倍

2. **max_overflow**
   - 默认值：10
   - 说明：允许超出 pool_size 的连接数
   - 建议：设置为 pool_size 的 50%

3. **pool_timeout**
   - 默认值：30
   - 说明：等待连接的超时时间（秒）
   - 建议：根据应用响应时间要求调整

4. **pool_recycle**
   - 默认值：3600
   - 说明：连接最大使用时间（秒）
   - 建议：根据数据库配置调整，避免连接超时

### 性能优化

1. **batch_size**
   - 默认值：1000
   - 说明：批量操作的记录数
   - 建议：根据数据量和内存使用情况调整

2. **echo**
   - 默认值：false
   - 说明：是否打印 SQL 语句
   - 建议：开发环境可设为 true，生产环境设为 false

## 使用示例

### 基本配置
```yaml
database:
  url: sqlite+aiosqlite:///data/graylink.db
  pool_size: 20
  max_overflow: 10
  pool_timeout: 30
  pool_recycle: 3600
  echo: false
  batch_size: 1000
```

### 高性能配置
```yaml
database:
  url: postgresql+asyncpg://user:pass@localhost/graylink
  pool_size: 50
  max_overflow: 25
  pool_timeout: 60
  pool_recycle: 7200
  echo: false
  batch_size: 2000
```

### 开发环境配置
```yaml
database:
  url: sqlite+aiosqlite:///data/graylink.db
  pool_size: 5
  max_overflow: 5
  pool_timeout: 10
  pool_recycle: 1800
  echo: true
  batch_size: 500
```

## 监控指标

系统提供以下数据库监控指标：

1. **连接池状态**
   - 当前连接数
   - 活动连接数
   - 空闲连接数
   - 等待连接数

2. **性能指标**
   - 查询执行时间
   - 慢查询统计
   - 连接使用率
   - 连接等待时间

3. **会话统计**
   - 活动会话数
   - 总会话数
   - 失败会话数
   - 平均会话时间

## 最佳实践

1. **连接池配置**
   - 根据实际负载调整 pool_size
   - 设置合理的 max_overflow 避免资源耗尽
   - 配置适当的超时时间

2. **性能优化**
   - 使用批量操作减少数据库交互
   - 合理设置 batch_size
   - 开启查询缓存减少数据库负载

3. **监控告警**
   - 监控连接池使用情况
   - 设置慢查询告警
   - 跟踪会话状态

4. **安全建议**
   - 使用环境变量管理敏感配置
   - 限制数据库连接权限
   - 定期更新数据库密码
``` 