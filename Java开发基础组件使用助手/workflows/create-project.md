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

明确以下信息：
- **项目名称**（如：user-service）
- **包名**（如：com.example.userservice）
- **功能模块**（规划需要哪些业务模块）
- **技术栈**：
  - JDK 17
  - Spring Boot 3.2.7
  - JDevelops 框架

---

## 步骤2：配置项目依赖

参考 GitHub 仓库中的示例项目配置：https://github.com/en-o/Jdevelops

### 核心依赖（pom.xml）

```xml
<properties>
    <java.version>17</java.version>
    <spring-boot.version>3.2.7</spring-boot.version>
    <jdevelops.version>最新版本</jdevelops.version>
</properties>

<dependencies>
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

    <!-- MySQL 驱动 -->
    <dependency>
        <groupId>com.mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
    </dependency>

    <!-- 可选：Redis + JWT 鉴权 -->
    <dependency>
        <groupId>cn.tannn.jdevelops</groupId>
        <artifactId>jdevelops-authentications-rjwt</artifactId>
        <version>${jdevelops.version}</version>
    </dependency>

    <!-- 可选：自动建库 -->
    <dependency>
        <groupId>cn.tannn.jdevelops</groupId>
        <artifactId>jdevelops-dals-autoschema</artifactId>
        <version>${jdevelops.version}</version>
    </dependency>
</dependencies>
```

**查看最新版本**：https://github.com/en-o/Jdevelops/releases

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
