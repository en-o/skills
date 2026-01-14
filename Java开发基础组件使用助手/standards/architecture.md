# 架构规范

## 核心原则

JDevelops 框架采用**垂直领域驱动**的分层架构，每个业务模块自包含 Entity、DAO、Service、ServiceImpl，控制器层独立按业务域划分。

---

## 标准目录结构

```
src/main/java/{package}/
├── common/                    # 公共组件层
│   ├── exception/            # 自定义异常（IException、IExceptionEnum）
│   └── pojo/                 # 公共POJO（JpaCommonBean、TableIdVO等）
│
├── controller/               # 控制器层（按业务域垂直划分）
│   ├── front/               # 前台业务控制器
│   │   ├── dto/            # 请求类（UserAdd、UserEdit等）
│   │   └── vo/             # 响应类（UserInfo等，仅在需要时创建）
│   ├── user/                # 用户管理控制器
│   ├── sys/                 # 系统管理控制器
│   └── logs/                # 日志管理控制器
│
├── {业务模块}/              # 业务领域模块（垂直拆分）
│   ├── constant/            # 业务常量/枚举
│   ├── entity/              # 实体类（JPA实体）
│   ├── dao/                 # 数据访问层接口
│   ├── service/             # 服务接口
│   ├── service/impl/        # 服务实现
│   └── domain/              # 领域对象（可选）
│
├── customer/                # 示例:用户业务模块
├── sys/                     # 示例:系统配置模块
├── logs/                    # 示例:日志模块
│
├── initialize/              # 初始化配置
└── util/                    # 工具类
```

---

## 架构核心特点

### 1. 垂直领域驱动

每个业务模块（customer、sys、logs等）**自包含**完整的分层结构：

```
customer/
├── entity/          # 实体类
├── dao/             # 数据访问接口
├── service/         # 服务接口
└── service/impl/    # 服务实现
```

**优点**：
- 模块边界清晰
- 易于维护和扩展
- 减少模块间耦合

### 2. 控制器独立

Controller 层按业务域划分，包含对应的请求/响应类：

```
controller/user/
├── dto/                    # 请求类
│   ├── UserAdd.java       # 新增请求
│   ├── UserEdit.java      # 编辑请求
│   └── UserPage.java      # 分页查询请求
├── vo/                     # 响应类（仅在需要时创建）
│   └── UserInfo.java      # 脱敏后的用户信息
└── CustomerController.java
```

**注意**：
- 目录名保留 `dto/` 和 `vo/`（历史兼容）
- 类名**严格遵循意图命名规范**，不带 VO/DTO 后缀

### 3. 跨模块调用

```
controller.user.CustomerController
    ↓ 注入
customer.service.CustomerService
    ↓ 实现
customer.service.impl.CustomerServiceImpl
    ↓ 注入
customer.dao.CustomerDao
    ↓ 操作
customer.entity.Customer
```

---

## 分层职责

### Controller 层

**职责**：
- 接收 HTTP 请求
- 参数验证
- 调用 Service 处理业务逻辑
- 返回统一格式的响应

**规范**：
- 使用 `@PathRestController("{path}")` 注解
- 不包含业务逻辑
- 不直接操作数据库
- 统一返回 `ResultVO<T>` 或 `ResultPageVO<T, JpaPageResult<T>>`

### Service 层

**职责**：
- 业务逻辑处理
- 事务控制
- 调用 DAO 操作数据库
- 数据转换和组装

**规范**：
- 接口继承 `J2Service<Entity>`
- 实现类继承 `J2ServiceImpl<Entity>`
- 使用 `@Service` 注解
- 使用构造器注入 DAO

### DAO 层

**职责**：
- 数据库访问
- CRUD 操作
- 自定义查询

**规范**：
- 接口继承 `JpaRepository<Entity, Long>`
- 使用 JPA 命名规范（findByXxx、existsByXxx 等）
- 复杂查询使用 `@Query` 注解

### Entity 层

**职责**：
- 数据模型定义
- 数据库表映射
- 字段验证规则

**规范**：
- 继承 `JpaCommonBean` 或 `JpaCommonBean2`
- 使用 JPA 注解（@Entity、@Table、@Column）
- 使用 `@Getter @Setter`（禁止 @Data）

---

## 包路径规范

### MUST 遵守的规则

| 层次 | 包路径规范 | 示例 |
|------|-----------|------|
| Controller | `{package}.controller.{domain}` | `com.example.controller.user` |
| Entity | `{package}.{module}.entity` | `com.example.customer.entity` |
| DAO | `{package}.{module}.dao` | `com.example.customer.dao` |
| Service | `{package}.{module}.service` | `com.example.customer.service` |
| ServiceImpl | `{package}.{module}.service.impl` | `com.example.customer.service.impl` |

### 完整示例

```
com.example.userservice/
├── controller/
│   └── user/
│       ├── dto/
│       │   ├── UserAdd.java
│       │   └── UserEdit.java
│       ├── vo/
│       │   └── UserInfo.java
│       └── CustomerController.java
│
└── customer/
    ├── entity/
    │   └── Customer.java
    ├── dao/
    │   └── CustomerDao.java
    ├── service/
    │   └── CustomerService.java
    └── service/impl/
        └── CustomerServiceImpl.java
```

---

## 分层调用规范

### ✅ 允许的调用

- Controller → Service
- Service → DAO
- Service → Service（同模块或跨模块）

### ❌ 禁止的调用

- **Controller → DAO**（跨层调用）
- **Controller → Entity**（跨层调用，除了作为参数和返回值）
- **循环依赖**（Service A → Service B → Service A）

---

## 模块化原则

### 高内聚

每个模块包含完整的业务功能，内部高度内聚：

```
customer/
├── entity/Customer.java
├── dao/CustomerDao.java
├── service/CustomerService.java
└── service/impl/CustomerServiceImpl.java
```

### 低耦合

模块间通过 Service 接口通信，避免直接依赖实现：

```java
// ✅ 正确：依赖接口
@PathRestController("order")
public class OrderController {
    private final OrderService orderService;
    private final CustomerService customerService;  // 跨模块调用

    public OrderController(OrderService orderService,
                          CustomerService customerService) {
        this.orderService = orderService;
        this.customerService = customerService;
    }
}

// ❌ 错误：依赖实现类
private final CustomerServiceImpl customerService;
```

---

## 依赖注入规范

### ✅ 使用构造器注入

```java
@PathRestController("user")
public class CustomerController {
    private final CustomerService customerService;

    // 构造器注入
    public CustomerController(CustomerService customerService) {
        this.customerService = customerService;
    }
}
```

### ❌ 避免字段注入

```java
// 避免使用 @Autowired 字段注入
@Autowired
private CustomerService customerService;
```

**原因**：
- 构造器注入更易于测试
- 依赖关系更明确
- 避免空指针异常

---

## 技术栈规范

### 核心框架

- **框架**：JDevelops（源码：https://github.com/en-o/Jdevelops）
- **构建工具**：Maven
- **JDK版本**：17+
- **Spring Boot**：3.2.7+
- **ORM**：Spring Data JPA

### 数据访问层

- `jdevelops-dals-jpa`：JPA数据访问层封装
- `jdevelops-dals-autoschema`：自动建库（可选）
- `jdevelops-dals-jdbctemplate`：JDBC增强（可选）

### 其他组件

- **数据库**：MySQL（mysql-connector-j）
- **缓存/鉴权**：jdevelops-authentications-rjwt（Redis + JWT）
- **API文档**：Swagger 3（OpenAPI 3.0）

---

## 依赖配置

### 核心依赖

```xml
<!-- JDevelops 核心 Starter -->
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-spring-boot-starter</artifactId>
    <!-- 内置 spring-boot-starter-web、jpa 等 -->
</dependency>

<!-- 数据库操作（已包含在 starter 中） -->
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-dals-jpa</artifactId>
    <!-- 提供 J2Service、J2ServiceImpl 等 -->
</dependency>
```

### 可选依赖

```xml
<!-- 自动建库 -->
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-dals-autoschema</artifactId>
    <!-- 启动时自动创建数据库（仅用于建库，不负责表操作） -->
</dependency>

<!-- Redis + JWT 鉴权 -->
<dependency>
    <groupId>cn.tannn.jdevelops</groupId>
    <artifactId>jdevelops-authentications-rjwt</artifactId>
    <!-- 登录鉴权、token管理 -->
</dependency>
```

查看最新版本：https://github.com/en-o/Jdevelops/releases

---

## 参考资源

- 框架源码：https://github.com/en-o/Jdevelops
- 官方文档：https://www.yuque.com/tanning/yg9ipo
- 命名规范：[./naming.md](./naming.md)
- Lombok 规范：[./lombok.md](./lombok.md)
