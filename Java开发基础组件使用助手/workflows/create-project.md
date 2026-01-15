# 创建新项目工作流

## 工作流清单

复制此清单并跟踪进度：

```
项目创建进度：
- [ ] 步骤1：项目路径确认（确定在哪里创建项目）
- [ ] 步骤2：收集项目信息（项目名、包路径、描述）
- [ ] 步骤3：选择组件和依赖（必要/推荐/可选）
- [ ] 步骤4：创建项目结构（目录和配置文件）
- [ ] 步骤5：生成基础代码（实体、配置类等）
- [ ] 步骤6：验证项目（编译、运行）
```

---

## 步骤1：项目路径确认（优先级最高）

### ⚠️ 必须首先确认项目创建位置

**在开始任何项目创建操作前，必须首先确认项目路径**：

#### 询问方式

- **询问**: 是否在当前目录下直接创建项目？
  - 当前工作目录会动态显示

#### 选项说明

**选项 A: 在当前目录下创建**
- 将在当前目录直接创建项目结构
- 适用场景：当前目录为空或专门用于新项目

**选项 B: 创建新目录**
- **继续询问**: 请提供项目目录名
- **示例**:
  - `my-project` → 将在当前目录下创建 `my-project/` 目录
  - `user-management-system` → 创建 `user-management-system/` 目录

**选项 C: 指定完整路径**
- **继续询问**: 请提供项目的完整路径
- **示例**:
  - Linux/Mac: `/home/user/projects/my-project`
  - Windows: `C:\work\projects\my-project`
  - 相对路径: `../../projects/my-project`

### 路径验证

在确认路径后，执行以下验证：

1. **检查路径是否存在**
   - 如果路径不存在，询问是否创建
   - 如果路径存在但非空，警告用户并确认是否继续

2. **检查写入权限**
   - 验证是否有创建文件和目录的权限
   - 如果没有权限，提示用户并重新询问路径

3. **检查是否已是项目目录**
   - 检查是否已包含 `pom.xml`、`build.gradle` 或 `src/` 目录
   - 如果是，警告用户可能覆盖现有项目，确认是否继续

### 确认后的操作

- 记录项目根路径
- 切换到项目根目录（如果需要）
- 准备创建项目结构

---

## 步骤2：收集项目信息

### ⚠️ 交互式询问

**如果用户未提供以下信息，必须进行询问**：

#### 1. 项目基本信息

**项目名称（artifactId）**：
- **询问**: 请提供项目名称（英文，用于 Maven artifactId）
- **说明**: 通常使用小写字母和连字符
- **示例**:
  - `user-management`
  - `order-system`
  - `blog-platform`

**包路径（groupId + basePackage）**：
- **询问**: 请提供项目包路径
- **说明**: 通常使用公司域名倒序 + 项目名
- **示例**:
  - `com.company.usermanagement`
  - `cn.tannn.order`
  - `org.example.blog`

**项目版本**：
- 默认: `1.0.0-SNAPSHOT`
- 可询问是否需要自定义版本号

#### 2. 项目描述和业务场景

- **询问**: 请描述您的项目是做什么的？有哪些主要功能模块？
- **说明**: 了解项目整体情况，帮助规划模块结构
- **示例回答**:
  - "这是一个管理后台系统，需要基础的用户、字典、角色、权限、菜单等功能"
  - "这是一个电商平台，需要商品管理、订单管理、用户管理等模块"
  - "这是一个内容管理系统，需要文章、分类、标签、评论等功能"

#### 3. Spring Boot 版本

- **默认**: 3.2.7（推荐）
- **询问**: 是否使用默认的 Spring Boot 3.2.7 版本？
  - 如果否，询问具体版本号

#### 4. JDK 版本

- **默认**: JDK 17（Spring Boot 3.x 要求）
- **说明**: Spring Boot 3.x 要求 JDK 17 或更高版本

#### 5. 数据库类型

- **询问**: 请选择数据库类型
- **选项**:
  - MySQL（推荐）
  - PostgreSQL
  - MariaDB
  - H2（测试）

#### 6. 包结构选择

- **询问**: 请选择您希望使用的包结构
- **选项**:

  - **选项 A - 传统三层架构（推荐小型项目）**:
    ```
    src/main/java/{basePackage}/
    ├── controller/{domain}/     # 控制器层
    ├── entity/                 # 实体层
    ├── dao/                    # DAO 层
    ├── service/                # Service 接口
    └── service/impl/           # Service 实现
    ```
    - **适用**: < 50 个实体的项目

  - **选项 B - 垂直切分（推荐中型项目）**:
    ```
    src/main/java/{basePackage}/
    ├── controller/{domain}/
    └── {module}/               # 业务模块
        ├── entity/
        ├── dao/
        ├── service/
        └── service/impl/
    ```
    - **适用**: 50-100 个实体，模块独立性强

  - **选项 C - 标准目录结构（推荐大型项目）**:
    ```
    src/main/java/{basePackage}/
    ├── controller/{domain}/
    ├── common/                 # 公共组件
    ├── core/                   # 核心配置
    └── modules/                # 业务模块
        └── {module}/
            └── {submodule}/
    ```
    - **适用**: > 100 个实体，多团队协作

- **说明**: 详细说明请参考 [../reference/package-structure.md](../reference/package-structure.md)

### 信息确认

在开始创建项目前，确认以下信息：
- [ ] **项目路径已确认并验证**
- [ ] 项目名称（artifactId）已明确
- [ ] 包路径（groupId + basePackage）已明确
- [ ] 项目描述和业务场景已明确
- [ ] Spring Boot 版本已确定
- [ ] 数据库类型已选择
- [ ] 包结构选择已确定（A/B/C）

---

## 步骤3：选择组件和依赖

### 组件选择

参考：[../reference/components.md](../reference/components.md)

#### 🔴 核心组件（必要）

以下组件会自动添加，无需询问：
- `jdevelops-spring-boot-starter`
- `jdevelops-dals-jpa`
- `jdevelops-apis-exception`（包含 jdevelops-apis-result）
- `spring-boot-starter-data-jpa`
- 数据库驱动（根据步骤2选择的数据库）

#### 🟡 推荐组件（强烈建议）

- **询问**: 是否添加以下推荐组件？
  - `jdevelops-apis-knife4j`（API 文档，强烈推荐）

#### 🟢 功能组件（按需选择）

- **询问**: 是否需要以下功能？
  - 用户认证和权限管理？
    - 是 → 添加 `jdevelops-authentications-rjwt`（Redis + JWT）
    - 或 → 添加 `jdevelops-authentications-jwt`（纯 JWT）
  - 文件上传和存储？
    - 是 → 添加 `jdevelops-files-sdk`
  - Excel 导入导出？
    - 是 → 添加 `jdevelops-utils-excel`
  - 缓存支持？
    - 是 → 添加 `jdevelops-dals-redis`
  - 日志增强？
    - 是 → 添加 `jdevelops-logs-login`（登录日志）
    - 和/或 → 添加 `jdevelops-logs-audit`（审计日志）

### 版本查询

使用版本查询工具获取最新版本：
```bash
cd scripts
python3 query_versions.py
```

或使用 Web API 查询：
```bash
python3 query_versions.py -a jdevelops-spring-boot-starter
```

### 依赖确认

- [ ] 所有依赖已选择
- [ ] 组件版本已确定
- [ ] 依赖兼容性已验证

---

## 步骤4：创建项目结构

### 创建目录结构

根据步骤2选择的包结构，创建对应的目录：

```bash
# 项目根目录
mkdir -p {projectPath}
cd {projectPath}

# Maven 标准目录
mkdir -p src/main/java/{basePackage}
mkdir -p src/main/resources
mkdir -p src/test/java/{basePackage}
mkdir -p src/test/resources

# 根据包结构创建子目录
# 选项 A/B/C 对应不同的目录结构
```

### 创建配置文件

#### 1. pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.7</version>
        <relativePath/>
    </parent>

    <groupId>{groupId}</groupId>
    <artifactId>{artifactId}</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <name>{projectName}</name>
    <description>{projectDescription}</description>

    <properties>
        <java.version>17</java.version>
        <jdevelops.version>查询到的最新版本</jdevelops.version>
    </properties>

    <dependencies>
        <!-- 核心依赖 -->
        <!-- 根据步骤3选择的组件添加 -->
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

#### 2. application.yml

```yaml
spring:
  application:
    name: {projectName}
  datasource:
    url: jdbc:mysql://localhost:3306/{dbName}?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password:
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        format_sql: true

server:
  port: 8080

# Knife4j 配置（如果添加了该组件）
knife4j:
  enable: true
  setting:
    language: zh_cn
```

#### 3. 启动类

```java
package {basePackage};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

---

## 步骤5：生成基础代码

### 创建公共组件

#### 1. 异常处理器（如果使用 jdevelops-apis-exception）

参考：[../guides/exception.md](../guides/exception.md)

#### 2. 配置类

```java
package {basePackage}.config;

import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {
    // 配置内容
}
```

### 创建示例模块（可选）

- **询问**: 是否需要创建一个示例模块（如 User 模块）？
  - 是 → 按照 [./add-module.md](./add-module.md) 工作流创建示例模块
  - 否 → 跳过，项目创建完成

---

## 步骤6：验证项目

### 编译验证

```bash
cd {projectPath}
mvn clean compile
```

### 运行验证

```bash
mvn spring-boot:run
```

### 访问验证

- 应用启动：http://localhost:8080
- API 文档（如果安装了 Knife4j）：http://localhost:8080/doc.html

### 验证清单

- [ ] 项目可以正常编译
- [ ] 项目可以正常启动
- [ ] 数据库连接正常
- [ ] API 文档可以访问（如果安装了 Knife4j）
- [ ] 没有依赖冲突或版本问题

---

## ✅ 完成标志

当以下所有项都完成时，项目创建完成：

- [ ] 项目路径已确认并验证
- [ ] 项目结构已创建
- [ ] 配置文件已生成
- [ ] 依赖已添加
- [ ] 项目可以正常编译和运行
- [ ] 符合 JDevelops 框架规范

---

## 📚 后续步骤

项目创建完成后，可以：

1. **添加业务模块** → 参考 [./add-module.md](./add-module.md)
2. **配置认证鉴权** → 参考 [../guides/authentication.md](../guides/authentication.md)
3. **集成其他功能** → 参考 [../guides/](../guides/)

---

## 📚 相关参考

- 组件清单：[../reference/components.md](../reference/components.md)
- 包结构指南：[../reference/package-structure.md](../reference/package-structure.md)
- 架构规范：[../standards/architecture.md](../standards/architecture.md)
- 完整示例：[../examples/complete-module.md](../examples/complete-module.md)
