# 项目配置文件指南

## 配置文件结构

项目使用多环境配置文件方式：
- `application.yaml` - 主配置文件（公共配置）
- `application-dev.yaml` - 开发环境配置
- `application-prod.yaml` - 生产环境配置

**注意**：统一使用 `.yaml` 扩展名，而不是 `.yml`

---

## application.yaml（主配置文件）

主配置文件包含所有环境通用的配置项：

```yaml
spring:
  application:
    name: your-project-name
  profiles:
    # 激活的环境配置（dev/prod）
    active: ${CONFIG_ENV:dev}
  mvc:
    throw-exception-if-no-handler-found: true
  servlet:
    multipart:
      # 文件上传配置
      enabled: true
      max-file-size: ${FILE_MAX_SIZE:500MB}
      max-request-size: ${FILE_MAX_REQUEST:500MB}

# JDevelops 框架配置
sunway:
  # Swagger 文档配置
  swagger:
    base-package:
      - com.example.project.controller
    title: ${spring.application.name}
    display-name: 基础接口
    group-name: a-basisapi

  # JWT 认证配置
  jwt:
    # JWT 密钥（生产环境必须修改！）
    token-secret: b4c33a6f172f13f91500b6c437a78d2cc5e5e9973e7dee431a1e8c34e68d365a
    # Web JWT 配置
    web:
      interceptor:
        # 放行路径（不需要 Token 验证）
        exclude-path-patterns:
          - /login
          - /logout
          - /error
    # 是否验证平台（防止 Web Token 访问 App 接口）
    verify-platform: true
    # JWT 前缀
    prefix: ${spring.application.name}

  # 登录限制配置
  login:
    limit:
      prefix: ${sunway.jwt.prefix}

  # Redis 缓存配置
  redis:
    cache:
      specs:
        statistic:
          ttl-minutes: 1
          prefix: ${sunway.jwt.prefix}-statistic

# 接口文档配置
knife4j:
  enable: true
  setting:
    language: zh-CN
    custom-code: 500
    enable-footer-custom: false
    enable-dynamic-parameter: true

# 验证码配置
captcha:
  cache: redis
  prefix: ${sunway.jwt.prefix}
  expire-time: 60
```

---

## application-dev.yaml（开发环境配置）

开发环境配置文件：

```yaml
# 服务器配置
server:
  port: ${serverPort:8080}

# 数据库配置
spring:
  # Redis 配置
  data:
    redis:
      database: ${REDIS_DB:0}
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PWD:}

  # MySQL 数据源配置
  datasource:
    username: ${MYSQL_UNM:root}
    password: ${MYSQL_PWD:root}
    # P6Spy 监控（开发环境用于 SQL 日志）
    driver-class-name: com.p6spy.engine.spy.P6SpyDriver
    url: jdbc:p6spy:mysql://${mysqlUrl:localhost:3306}/${databases:your_db}?useUnicode=true&characterEncoding=UTF8&zeroDateTimeBehavior=convertToNull&allowMultiQueries=true&useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true
    hikari:
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
      maximum-pool-size: 15
      pool-name: ${spring.application.name}
      minimum-idle: 15

  # JPA 配置
  jpa:
    hibernate:
      # 开发环境自动更新表结构
      ddl-auto: update
    open-in-view: false
    database: mysql

# 监控端点配置
management:
  endpoints:
    web:
      exposure:
        # 开发环境暴露所有监控端点
        include:
          - "*"
        exclude:
          - shutdown
          - sessions
  metrics:
    tags:
      application: ${spring.application.name}
```

---

## application-prod.yaml（生产环境配置）

生产环境配置文件：

```yaml
# 服务器配置
server:
  port: ${serverPort:8080}

# 数据库配置
spring:
  # Redis 配置
  data:
    redis:
      database: ${REDIS_DB:0}
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PWD:}

  # MySQL 数据源配置
  datasource:
    username: ${MYSQL_UNM:root}
    password: ${MYSQL_PWD:root}
    # 生产环境使用标准 MySQL 驱动
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://${mysqlUrl:localhost:3306}/${databases:your_db}?useUnicode=true&characterEncoding=UTF8&zeroDateTimeBehavior=convertToNull&allowMultiQueries=true&useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true
    hikari:
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
      maximum-pool-size: 15
      pool-name: ${spring.application.name}
      minimum-idle: 15

  # JPA 配置
  jpa:
    hibernate:
      # 生产环境不自动修改表结构
      ddl-auto: none
    open-in-view: false
    database: mysql

# 监控端点配置
management:
  endpoints:
    web:
      exposure:
        # 生产环境只暴露必要的监控端点
        include:
          - info
          - health
        exclude:
          - shutdown
          - sessions
          - beans
          - env
  metrics:
    tags:
      application: ${spring.application.name}

# 接口文档配置
knife4j:
  enable: true
  # 生产环境启用文档访问认证
  basic:
    enable: true
    username: ${DOC_USERNAME:admin}
    password: ${DOC_PASSWORD:admin123}
    include:
      - /v3/api-docs
```

---

## JWT 配置说明

### ⚠️ 重要：无需创建 JwtConfig 类

**JDevelops 框架已经内置了 JWT 配置支持**，只需要在 `application.yaml` 中配置即可，**无需手动创建 JwtConfig 配置类**。

### JWT 配置项详解

```yaml
sunway:
  jwt:
    # JWT 密钥（必须配置）
    # ⚠️ 生产环境务必修改为强密钥！
    token-secret: your-secret-key-at-least-32-characters-long

    # JWT 前缀（用于 Redis key 前缀）
    prefix: your-project-name

    # 是否验证平台（推荐开启）
    # 防止 Web Token 访问 App 接口，或 App Token 访问 Web 接口
    verify-platform: true

    # Web JWT 拦截器配置
    web:
      interceptor:
        # 放行路径（不需要 Token 验证的接口）
        exclude-path-patterns:
          - /login          # 登录接口
          - /logout         # 登出接口
          - /register       # 注册接口
          - /error          # 错误页面
          - /captcha        # 验证码接口
          - /v3/api-docs/** # Swagger 文档
          - /swagger-ui/**  # Swagger UI
```

### Token 密钥生成

生产环境必须使用强密钥，可以使用以下方式生成：

```bash
# 使用 OpenSSL 生成 64 位随机密钥
openssl rand -hex 32

# 或使用 Java 代码生成
# java -c "System.out.println(java.util.UUID.randomUUID().toString().replace(\"-\",\"\") + java.util.UUID.randomUUID().toString().replace(\"-\",\"\"));"
```

### 平台验证说明

当 `verify-platform: true` 时，框架会验证 Token 中的平台标识：
- Web Token 只能访问 Web 接口
- App Token 只能访问 App 接口
- 防止跨平台攻击

---

## 环境变量配置

配置文件支持使用环境变量，格式：`${ENV_NAME:default_value}`

### 常用环境变量

```bash
# 环境选择
export CONFIG_ENV=prod

# 服务器端口
export serverPort=8080

# MySQL 配置
export mysqlUrl=localhost:3306
export databases=your_database
export MYSQL_UNM=root
export MYSQL_PWD=your_password

# Redis 配置
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=0
export REDIS_PWD=your_redis_password

# 文件上传配置
export FILE_MAX_SIZE=500MB
export FILE_MAX_REQUEST=500MB

# 文档访问认证
export DOC_USERNAME=admin
export DOC_PASSWORD=secure_password
```

---

## 配置文件最佳实践

### 1. 配置分离原则

- **公共配置** → `application.yaml`
- **环境特定配置** → `application-{env}.yaml`
- **敏感信息** → 使用环境变量

### 2. 安全配置

```yaml
# ❌ 错误：敏感信息硬编码
sunway:
  jwt:
    token-secret: 123456  # 太弱！

spring:
  datasource:
    password: root  # 硬编码密码！

# ✅ 正确：使用环境变量
sunway:
  jwt:
    token-secret: ${JWT_SECRET}  # 从环境变量读取

spring:
  datasource:
    password: ${MYSQL_PWD}  # 从环境变量读取
```

### 3. 开发与生产环境差异

| 配置项 | 开发环境 | 生产环境 |
|--------|----------|----------|
| 数据库驱动 | P6SpyDriver（SQL 日志） | MySQL Driver |
| JPA ddl-auto | update（自动更新表） | none（不修改表） |
| 监控端点 | 暴露所有 | 仅暴露必要的 |
| 文档访问 | 无需认证 | 需要认证 |
| 日志级别 | DEBUG | INFO/WARN |

### 4. 配置验证清单

创建项目配置文件后，检查以下项：

- [ ] JWT 密钥已修改为强密钥
- [ ] 数据库连接信息正确
- [ ] Redis 连接信息正确
- [ ] 敏感信息使用环境变量
- [ ] 生产环境 `ddl-auto` 设置为 `none`
- [ ] 文件上传大小限制合理
- [ ] 监控端点暴露合理
- [ ] 接口文档访问权限配置正确

---

## 参考资源

- 组件配置：[../reference/components.md](../reference/components.md)
- 官方文档：https://www.yuque.com/tanning/yg9ipo
