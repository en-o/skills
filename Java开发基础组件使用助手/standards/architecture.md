# 架构规范

## 核心原则

JDevelops 框架支持**灵活的分层架构**，根据项目规模选择合适的目录结构：
- **小型项目**：传统三层架构（entity、dao、service 集中管理）
- **中型项目**：垂直切分（按模块划分，模块内三层架构）
- **大型项目**：标准目录结构（controller + common + core + modules）

---

## 标准目录结构（推荐用于大型项目）

这是实际大型项目中广泛采用的标准结构，适合复杂业务场景。

```
src/main/java/{package}/
├── controller/               # 控制器层（统一管理，按业务域划分）
│   ├── user/                # 用户领域控制器
│   │   ├── dto/            # 请求类（UserAdd、UserEdit、UserPage等）
│   │   ├── vo/             # 响应类（UserInfo等，仅在需要时创建）
│   │   └── UserController.java
│   ├── sys/                 # 系统管理控制器
│   ├── logs/                # 日志管理控制器
│   └── front/               # 前台业务控制器
│
├── common/                   # 公共组件层
│   ├── annotations/         # 自定义注解
│   ├── constant/            # 公共常量/枚举
│   ├── pojo/                # 公共POJO（JpaCommonBean、ResultVO等）
│   ├── util/                # 工具类
│   ├── query/               # 公共查询对象
│   ├── sensitive/           # 敏感信息处理
│   └── views/               # JsonView 视图定义
│
├── core/                     # 核心配置层
│   ├── config/              # 配置类（Swagger、Redis、MongoDB等）
│   ├── exception/           # 全局异常处理
│   ├── initialize/          # 初始化类
│   └── redis/               # Redis 配置
│
└── modules/                  # 业务模块层（细粒度垂直切分）
    ├── account/             # 账户大模块
    │   ├── constant/        # 模块级常量
    │   ├── org/            # 组织子模块
    │   │   ├── entity/
    │   │   ├── dao/
    │   │   ├── service/
    │   │   └── service/impl/
    │   ├── role/           # 角色子模块
    │   │   ├── entity/
    │   │   ├── dao/
    │   │   ├── service/
    │   │   └── service/impl/
    │   ├── security/       # 安全子模块
    │   │   ├── entity/
    │   │   ├── dao/
    │   │   ├── service/
    │   │   └── service/impl/
    │   └── suser/          # 用户子模块
    │       ├── entity/
    │       ├── dao/
    │       ├── service/
    │       └── service/impl/
    │
    ├── biz/                 # 业务大模块
    │   └── {submodule}/    # 业务子模块
    │
    ├── file/                # 文件管理模块
    │   ├── entity/
    │   ├── dao/
    │   ├── service/
    │   └── service/impl/
    │
    └── logs/                # 日志模块
        ├── entity/
        ├── dao/
        ├── service/
        └── service/impl/
```

**结构特点**：
- **Controller 统一管理**：所有控制器按业务域划分在 controller 下
- **Common 公共层**：存放通用组件，被所有模块共享
- **Core 核心层**：框架配置和全局处理
- **Modules 模块层**：细粒度垂直切分，大模块下包含多个子模块，每个子模块内部采用传统架构

**更多包结构选择**，请参考：[../reference/package-structure.md](../reference/package-structure.md)

---

## 架构核心特点

### 1. 分层清晰

#### Controller 层（统一管理）
- 所有控制器集中在 `controller/{domain}/` 下
- 按业务域划分（user、sys、logs、front 等）
- 包含对应的 dto 和 vo

#### Common 层（公共组件）
- 通用注解、常量、POJO、工具类
- 被所有模块共享使用

#### Core 层（核心配置）
- 框架配置（Swagger、Redis、MongoDB 等）
- 全局异常处理
- 应用初始化逻辑

#### Modules 层（业务模块）
- 按大模块划分（account、biz、file、logs 等）
- 大模块下可包含多个子模块（如 account 下的 org、role、security、suser）
- 每个子模块内部采用传统架构（entity、dao、service、service/impl）

### 2. 模块化设计

每个子模块包含完整的业务逻辑：

```
account/org/          # 组织子模块
├── entity/          # 组织相关实体
├── dao/             # 组织数据访问
├── service/         # 组织服务接口
└── service/impl/    # 组织服务实现
```

**优点**：
- 模块边界清晰
- 易于维护和扩展
- 减少模块间耦合
- 便于团队分工

### 3. 跨模块调用

```
controller.user.UserController
    ↓ 注入
modules.account.suser.service.UserService
    ↓ 实现
modules.account.suser.service.impl.UserServiceImpl
    ↓ 注入
modules.account.suser.dao.UserDao
    ↓ 操作
modules.account.suser.entity.User
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

### 标准目录结构包路径

| 层次 | 包路径规范 | 示例 |
|------|-----------|------|
| Controller | `{package}.controller.{domain}` | `com.sunway.sxzz.controller.user` |
| DTO/VO | `{package}.controller.{domain}.dto/vo` | `com.sunway.sxzz.controller.user.dto` |
| 大模块 | `{package}.modules.{module}` | `com.sunway.sxzz.modules.account` |
| 子模块 Entity | `{package}.modules.{module}.{submodule}.entity` | `com.sunway.sxzz.modules.account.suser.entity` |
| 子模块 DAO | `{package}.modules.{module}.{submodule}.dao` | `com.sunway.sxzz.modules.account.suser.dao` |
| 子模块 Service | `{package}.modules.{module}.{submodule}.service` | `com.sunway.sxzz.modules.account.suser.service` |
| 子模块 ServiceImpl | `{package}.modules.{module}.{submodule}.service.impl` | `com.sunway.sxzz.modules.account.suser.service.impl` |
| 公共组件 | `{package}.common.{component}` | `com.sunway.sxzz.common.pojo` |
| 核心配置 | `{package}.core.{component}` | `com.sunway.sxzz.core.config` |

### 其他包结构路径

**传统三层架构**：
- Entity: `{package}.entity`
- DAO: `{package}.dao`
- Service: `{package}.service`
- ServiceImpl: `{package}.service.impl`

**垂直切分（模块化）**：
- Entity: `{package}.{module}.entity`
- DAO: `{package}.{module}.dao`
- Service: `{package}.{module}.service`
- ServiceImpl: `{package}.{module}.service.impl`

详细说明请参考：[../reference/package-structure.md](../reference/package-structure.md)

### 完整示例（标准目录结构）

```
com.sunway.sxzz/
├── controller/
│   └── user/
│       ├── dto/
│       │   ├── UserAdd.java
│       │   └── UserEdit.java
│       ├── vo/
│       │   └── UserInfo.java
│       └── UserController.java
│
├── common/
│   ├── pojo/
│   │   └── JpaCommonBean.java
│   └── util/
│
├── core/
│   ├── config/
│   └── exception/
│
└── modules/
    └── account/
        └── suser/
            ├── entity/
            │   └── User.java
            ├── dao/
            │   └── UserDao.java
            ├── service/
            │   └── UserService.java
            └── service/impl/
                └── UserServiceImpl.java
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

每个子模块包含完整的业务功能，内部高度内聚：

```
modules/account/suser/
├── entity/User.java
├── dao/UserDao.java
├── service/UserService.java
└── service/impl/UserServiceImpl.java
```

### 低耦合

模块间通过 Service 接口通信，避免直接依赖实现：

```java
// ✅ 正确：依赖接口
@PathRestController("user")
public class UserController {
    private final UserService userService;
    private final OrganizationService organizationService;  // 跨子模块调用

    public UserController(UserService userService,
                         OrganizationService organizationService) {
        this.userService = userService;
        this.organizationService = organizationService;
    }
}

// ❌ 错误：依赖实现类
private final UserServiceImpl userService;
```

### 大模块规划

将相关子模块组织在大模块下：

```
modules/
├── account/          # 账户大模块
│   ├── suser/       # 用户子模块
│   ├── role/        # 角色子模块
│   ├── org/         # 组织子模块
│   └── security/    # 安全子模块
│
├── biz/             # 业务大模块
│   └── ...
│
└── file/            # 文件大模块（也可以不再细分子模块）
    ├── entity/
    ├── dao/
    ├── service/
    └── service/impl/
```

**原则**：
- 大模块按业务领域划分（如 account、biz、file、logs）
- 子模块进一步细化功能（如 suser、role、org、security）
- 如果大模块功能简单，可以不再细分子模块

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
