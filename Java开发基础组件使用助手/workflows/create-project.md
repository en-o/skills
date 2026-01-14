# 创建新项目工作流

## 工作流清单

```
项目创建进度：
- [ ] 步骤1：确定项目信息（名称、包名、功能）
- [ ] 步骤2：配置项目依赖（pom.xml）
- [ ] 步骤3：创建标准目录结构
- [ ] 步骤4：配置 application.yml
- [ ] 步骤5：创建初始化类
- [ ] 步骤6：验证项目启动
```

---

## 步骤1：确定项目信息

### ⚠️ 交互式询问

**如果用户未提供以下信息，必须进行询问**：

1. **项目名称**
   - 询问：请提供项目名称（例如：user-service、order-management）
   - 说明：用于创建项目目录和 Spring 应用名称
   - 示例：user-service

2. **包路径**
   - 询问：请提供 Java 包路径（例如：cn.tannn.example.userservice）
   - 说明：遵循反向域名规范
   - 示例：com.company.projectname

3. **项目描述**
   - 询问：请简要描述项目功能和业务场景
   - 说明：帮助规划模块结构和选择合适的组件
   - 示例：这是一个用户管理系统，需要实现用户注册、登录、权限控制等功能

4. **选择组件**
   - 询问：请选择需要集成的组件
   - 说明：根据项目需求选择，参考 [../reference/components.md](../reference/components.md)
   - 提示：
     - 🔴 必要组件（已自动包含）：jdevelops-spring-boot-starter、jdevelops-dals-jpa
     - 🟡 推荐组件：jdevelops-apis-result、springdoc-openapi
     - 🟢 可选组件：根据场景选择（认证、文件上传、Excel、缓存等）

### 项目信息确认

确认以下信息：
- **项目名称**：${用户提供或询问得到}
- **包名**：${用户提供或询问得到}
- **项目描述**：${用户提供或询问得到}
- **选择的组件**：${根据项目需求确定}
- **技术栈**：
  - JDK 17
  - Spring Boot 3.2.7
  - JDevelops 框架（最新版本）

---

## 步骤2：配置项目依赖

### 查询最新版本

**⚠️ 使用前必须查询最新版本号**

使用 Python 脚本查询 JDevelops 组件的最新版本：

```bash
cd scripts
python3 query_versions.py
```

查询特定组件：
```bash
python3 query_versions.py -a jdevelops-spring-boot-starter -f maven
```

**在线查询**: https://central.sonatype.com/search?q=cn.tannn.jdevelops

### 核心依赖（pom.xml）

参考 GitHub 仓库中的示例项目配置：https://github.com/en-o/Jdevelops

```xml
<properties>
    <java.version>17</java.version>
    <spring-boot.version>3.2.7</spring-boot.version>
    <!-- ⚠️ 替换为实际查询到的最新版本 -->
    <jdevelops.version>${实际最新版本}</jdevelops.version>
</properties>

<dependencies>
    <!-- 🔴 必要组件 -->

    <!-- JDevelops 核心 Starter -->
    <dependency>
        <groupId>cn.tannn.jdevelops</groupId>
        <artifactId>jdevelops-spring-boot-starter</artifactId>
        <version>${jdevelops.version}</version>
    </dependency>

    <!-- JPA 数据访问层 -->
    <dependency>
        <groupId>cn.tannn.jdevelops</groupId>
        <artifactId>jdevelops-dals-jpa</artifactId>
        <version>${jdevelops.version}</version>
    </dependency>

    <!-- Spring Data JPA -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>

    <!-- MySQL 驱动 -->
    <dependency>
        <groupId>com.mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
    </dependency>

    <!-- 🟡 推荐组件 -->

    <!-- 统一返回结果 -->
    <dependency>
        <groupId>cn.tannn.jdevelops</groupId>
        <artifactId>jdevelops-apis-result</artifactId>
        <version>${jdevelops.version}</version>
    </dependency>

    <!-- Swagger 文档 -->
    <dependency>
        <groupId>org.springdoc</groupId>
        <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
        <version>2.3.0</version>
    </dependency>

    <!-- 🟢 可选组件（根据步骤1选择的组件添加） -->

    <!-- Redis + JWT 鉴权 -->
    <dependency>
        <groupId>cn.tannn.jdevelops</groupId>
        <artifactId>jdevelops-authentications-rjwt</artifactId>
        <version>${jdevelops.version}</version>
    </dependency>

    <!-- 自动建库 -->
    <dependency>
        <groupId>cn.tannn.jdevelops</groupId>
        <artifactId>jdevelops-dals-autoschema</artifactId>
        <version>${jdevelops.version}</version>
    </dependency>

    <!-- 更多可选组件请参考 ../reference/components.md -->
</dependencies>
```

**组件选择参考**: [../reference/components.md](../reference/components.md)

---

## 步骤3：创建标准目录结构

参考：[../standards/architecture.md](../standards/architecture.md)

```
src/main/java/{package}/
├── common/                    # 公共组件
│   ├── exception/            # 自定义异常
│   └── pojo/                 # 公共POJO
│
├── controller/               # 控制器层
│   └── {domain}/            # 按业务域划分
│       ├── dto/
│       └── vo/
│
├── {module}/                # 业务模块
│   ├── constant/
│   ├── entity/
│   ├── dao/
│   ├── service/
│   └── service/impl/
│
├── initialize/              # 初始化配置
└── util/                    # 工具类
```

---

## 步骤4：配置 application.yml

```yaml
spring:
  application:
    name: ${项目名称}

  datasource:
    url: jdbc:mysql://localhost:3306/${数据库名}?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai
    username: ${用户名}
    password: ${密码}
    driver-class-name: com.mysql.cj.jdbc.Driver

  jpa:
    hibernate:
      ddl-auto: update  # 开发环境使用 update，生产环境使用 validate
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQLDialect
        format_sql: true

# Swagger 配置
springdoc:
  api-docs:
    enabled: true
  swagger-ui:
    enabled: true
    path: /swagger-ui.html
```

---

## 步骤5：创建初始化类

### 主启动类

```java
package ${package};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### 公共基类（可选）

参考 [../guides/entity.md](../guides/entity.md) 创建 `JpaCommonBean` 基类。

---

## 步骤6：验证项目启动

### 启动项目

```bash
mvn spring-boot:run
```

### 验证项目

- [ ] 项目启动成功
- [ ] 数据库连接正常
- [ ] Swagger UI 可访问（http://localhost:8080/swagger-ui.html）
- [ ] 日志输出正常

---

## 🎯 后续步骤

项目创建完成后，开始添加业务模块：[./add-module.md](./add-module.md)

---

## 📚 参考资源

- 框架源码：https://github.com/en-o/Jdevelops
- 官方文档：https://www.yuque.com/tanning/yg9ipo
- 架构规范：[../standards/architecture.md](../standards/architecture.md)
