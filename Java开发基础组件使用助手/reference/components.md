# JDevelops 组件清单

本文档列出 JDevelops 框架的所有可用组件，标注必要组件和可选组件，方便创建项目时选择。

## 组件分类

### 🔴 核心组件（必要）

这些组件是使用 JDevelops 框架的基础，创建项目时必须包含。

#### 1. jdevelops-spring-boot-starter
- **用途**: JDevelops 核心 Starter，提供框架基础功能
- **必要性**: ✅ 必需
- **Maven 依赖**:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-spring-boot-starter</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```

- **⚠️ 重要说明**: 此 Starter 已包含以下组件，**无需重复添加**：

  **数据访问层**:
  - `jdevelops-dals-jpa` - JPA 数据访问层支持

  **API 相关**:
  - `jdevelops-apis-exception` - 全局异常处理
  - `jdevelops-apis-knife4j` - Knife4j API 文档
  - `jdevelops-apis-log` - API 日志记录

  **日志组件**:
  - `jdevelops-logs-logback` - 日志增强
  - `jdevelops-logs-p6spy` - SQL 日志监控

  **工具类**:
  - `jdevelops-utils-validation` - 参数校验工具
  - `jdevelops-utils-spring` - Spring 工具类
  - `jdevelops-utils-core` - 核心工具类
  - `jdevelops-utils-http` - HTTP 工具类
  - `jdevelops-utils-time` - 时间处理工具

  **第三方依赖**:
  - `spring-boot-starter-web` - Spring Boot Web 支持
  - `commons-codec` - Apache Commons 编解码库

- **结论**: 使用 `jdevelops-spring-boot-starter` 后，上述组件都已自动引入，可直接使用，无需在 pom.xml 中重复声明。

#### 2. jdevelops-dals-jpa
- **用途**: JPA 数据访问层支持，提供 JpaCommonBean、J2Service 等基础类
- **必要性**: ✅ 必需
- **说明**: ⚠️ 此组件已被 `jdevelops-spring-boot-starter` 包含，**使用 starter 后无需单独添加**
- **Maven 依赖**（仅在纯 Spring Boot 项目中需要）:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-dals-jpa</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```

#### 3. Spring Boot Starter Data JPA
- **用途**: Spring Data JPA 支持
- **必要性**: ✅ 必需
- **Maven 依赖**:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
```

#### 4. jdevelops-apis-exception
- **用途**: 全局异常处理，统一返回结果封装（包含 jdevelops-apis-result）
- **必要性**: ✅ 必需
- **说明**:
  - ⚠️ 此组件已被 `jdevelops-spring-boot-starter` 包含，**使用 starter 后无需单独添加**
  - 这是最核心的组件，提供：
    - 全局异常捕获和处理
    - 统一的 API 返回格式（ResultVO、ResultPageVO）
    - BusinessException、TokenException 等内置异常
    - @DisposeException 自定义异常处理
    - **自动引入 jdevelops-apis-result**，无需单独添加
- **Maven 依赖**（仅在纯 Spring Boot 项目中需要）:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-apis-exception</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```
- **包含的依赖**: jdevelops-apis-result、jdevelops-utils-aop
- **详细文档**: [guides/exception.md](../guides/exception.md)

#### 5. 数据库驱动
- **用途**: 连接数据库
- **必要性**: ✅ 必需（根据使用的数据库选择）
- **Maven 依赖**:
```xml
<!-- MySQL -->
<dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
</dependency>

<!-- PostgreSQL -->
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
</dependency>
```

---

### 🟡 推荐组件（强烈建议）

这些组件不是必需的，但能显著提升开发效率和项目质量。

#### 6. jdevelops-apis-knife4j
- **用途**: Knife4j API 文档（基于 OpenAPI 3 和 Swagger）
- **必要性**: 🟡 强烈推荐
- **说明**:
  - ⚠️ 此组件已被 `jdevelops-spring-boot-starter` 包含，**使用 starter 后无需单独添加**
  - 增强版 Swagger UI，提供更美观的 API 文档
  - 支持在线调试、离线文档、授权配置等功能
  - 基于 knife4j-openapi3-jakarta-spring-boot-starter
- **Maven 依赖**（仅在纯 Spring Boot 项目中需要）:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-apis-knife4j</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```
- **访问地址**: http://localhost:8080/doc.html
- **官方文档**: https://doc.xiaominfo.com/

---

### 🟢 功能组件（按需选择）

根据项目实际需求选择以下组件。

#### 7. jdevelops-authentications-rjwt
- **用途**: Redis + JWT 认证鉴权
- **适用场景**: 需要用户认证、权限控制的系统
- **必要性**: 🟢 可选
- **Maven 依赖**:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-authentications-rjwt</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```
- **需要额外配置**: Redis

#### 8. jdevelops-authentications-jwt
- **用途**: JWT 认证（不依赖 Redis）
- **适用场景**: 需要认证但不想使用 Redis
- **必要性**: 🟢 可选
- **Maven 依赖**:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-authentications-jwt</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```

#### 9. jdevelops-dals-autoschema
- **用途**: 自动创建数据库 Schema
- **适用场景**: 开发环境快速建库，或需要多租户数据库隔离
- **必要性**: 🟢 可选
- **Maven 依赖**:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-dals-autoschema</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```

#### 10. jdevelops-utils-excel
- **用途**: Excel 导入导出
- **适用场景**: 需要数据导入导出功能
- **必要性**: 🟢 可选
- **Maven 依赖**:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-utils-excel</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```

#### 11. jdevelops-utils-oss
- **用途**: 对象存储（OSS/MinIO）集成
- **适用场景**: 需要文件上传、存储功能
- **必要性**: 🟢 可选
- **Maven 依赖**:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-utils-oss</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```

#### 12. jdevelops-utils-cache
- **用途**: 缓存支持（Redis、本地缓存）
- **适用场景**: 需要缓存加速
- **必要性**: 🟢 可选
- **Maven 依赖**:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-utils-cache</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```

#### 13. jdevelops-logs-logback
- **用途**: 日志增强（请求日志、操作日志）
- **适用场景**: 需要详细的日志记录
- **必要性**: 🟢 可选
- **说明**: ⚠️ 此组件已被 `jdevelops-spring-boot-starter` 包含，**使用 starter 后无需单独添加**
- **Maven 依赖**（仅在纯 Spring Boot 项目中需要）:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-logs-logback</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```

#### 14. jdevelops-webs-validator
- **用途**: 参数校验增强
- **适用场景**: 需要复杂的参数校验逻辑
- **必要性**: 🟢 可选
- **Maven 依赖**:
```xml
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-webs-validator</artifactId>
    <version>${jdevelops.version}</version>
</dependency>
```

---

## 常见场景推荐组合

### ⚠️ 重要提示

使用 `jdevelops-spring-boot-starter` 后，以下组件已自动包含，**无需在 pom.xml 中重复添加**：
- jdevelops-dals-jpa
- jdevelops-apis-exception
- jdevelops-apis-knife4j
- jdevelops-apis-log
- jdevelops-logs-logback
- jdevelops-logs-p6spy
- jdevelops-utils-validation
- jdevelops-utils-spring
- jdevelops-utils-core
- jdevelops-utils-http
- jdevelops-utils-time
- spring-boot-starter-web

**只需额外添加**：
- Spring Boot Starter Data JPA（数据库访问）
- 数据库驱动（MySQL/PostgreSQL 等）
- 其他可选功能组件（认证、缓存、Excel、OSS 等）

---

### 场景 1: 基础 CRUD 项目
适用于简单的增删改查系统，不需要认证、文件上传等功能。

**必选组件**:
- jdevelops-spring-boot-starter（已包含 JPA、异常处理、Knife4j、日志等）
- Spring Boot Starter Data JPA
- MySQL Connector（或其他数据库驱动）

**说明**: 使用 starter 后，基础功能已全部具备，无需额外添加其他组件

### 场景 2: 管理后台系统
适用于需要用户登录、权限控制的管理系统。

**必选组件**:
- jdevelops-spring-boot-starter（已包含 JPA、异常处理、Knife4j、日志等）
- Spring Boot Starter Data JPA
- MySQL Connector（或其他数据库驱动）

**额外添加**:
- jdevelops-authentications-rjwt（认证鉴权，需要 Redis）

**可选组件**:
- jdevelops-utils-excel（数据导出）
- jdevelops-utils-cache（缓存加速）

### 场景 3: 电商/内容平台
适用于需要文件上传、缓存的复杂业务系统。

**必选组件**:
- jdevelops-spring-boot-starter（已包含 JPA、异常处理、Knife4j、日志等）
- Spring Boot Starter Data JPA
- MySQL Connector（或其他数据库驱动）

**额外添加**:
- jdevelops-authentications-rjwt（认证鉴权）
- jdevelops-utils-oss（文件上传存储）
- jdevelops-utils-cache（缓存加速）

**可选组件**:
- jdevelops-utils-excel（数据导入导出）

### 场景 4: 微服务模块
适用于微服务架构中的单个服务。

**必选组件**:
- jdevelops-spring-boot-starter（已包含 JPA、异常处理、Knife4j、日志等）
- Spring Boot Starter Data JPA
- MySQL Connector（或其他数据库驱动）

**额外添加**:
- jdevelops-authentications-jwt（轻量级认证，不依赖 Redis）

---

## 版本查询

### 查询最新版本
使用 Python 脚本查询最新版本：
```bash
cd scripts
python3 query_versions.py
```

### 查询特定组件
```bash
python3 query_versions.py -a jdevelops-spring-boot-starter
```

### 生成 Maven 依赖
```bash
python3 query_versions.py -a jdevelops-spring-boot-starter -f maven
```

---

## 参考资源

- 框架源码: https://github.com/en-o/Jdevelops
- 官方文档: https://www.yuque.com/tanning/yg9ipo
- Maven Central: https://central.sonatype.com/search?q=cn.tannn.jdevelops
