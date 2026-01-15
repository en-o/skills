# 框架模式对比和代码规范

## 概述

本文档说明 JDevelops 框架和纯 Spring Boot 两种模式的区别，以及各自的代码生成规范。

---

## 🔍 框架检测机制

### 创建新项目

如果用户**未明确说明**使用 JDevelops 框架，必须询问：

```
"请问您希望使用哪种技术方案？

【选项 A】JDevelops 框架（推荐）
【选项 B】纯 Spring Boot

请选择 A 或 B"
```

### 现有项目添加功能

**自动检测**，无需询问用户：

1. 读取项目的 `pom.xml` 文件
2. 检测依赖：
   - 包含 `<groupId>cn.tannn.jdevelops</groupId>` → JDevelops 框架
   - 只有标准 Spring 依赖 → 纯 Spring Boot
3. 通知用户检测结果

**检测代码示例**：

```bash
# 读取 pom.xml
cat pom.xml | grep -A 2 "cn.tannn.jdevelops"
```

如果找到输出，则为 JDevelops 项目。

---

## 📊 两种模式对比

| 特性 | JDevelops 框架 | 纯 Spring Boot |
|-----|---------------|---------------|
| **基础框架** | Spring Boot 3.x + JDevelops | Spring Boot 3.x |
| **Entity 基类** | JpaCommonBean / JpaCommonBean2 | 自定义或无基类 |
| **Repository** | JpaRepository（标准） | JpaRepository（标准） |
| **Service 基类** | J2Service / J2ServiceImpl | 自定义接口或无 |
| **Controller 注解** | @PathRestController | @RestController |
| **返回格式** | ResultVO / ResultPageVO | 自定义或标准 ResponseEntity |
| **分页** | JpaPageResult | Spring Data Page |
| **异常处理** | 框架统一处理 | 自定义 @ControllerAdvice |
| **认证鉴权** | jdevelops-authentications-* | 自定义或 Spring Security |
| **API 文档** | Knife4j（jdevelops-apis-knife4j） | Springdoc OpenAPI |
| **推荐场景** | 快速开发、团队协作、企业应用 | 灵活定制、轻量级项目 |

---

## 📝 代码生成规范

### JDevelops 框架模式

#### Entity 层

```java
@Getter
@Setter
@Entity
@Table(name = "sys_user")
@Comment("用户表")
public class User extends JpaCommonBean {

    @Column(name = "login_name", nullable = false, unique = true, length = 50)
    @Comment("登录名")
    @Schema(description = "登录名")
    private String loginName;

    @Column(name = "password", nullable = false)
    @Comment("密码")
    @JsonIgnore
    private String password;

    @Column(name = "role_id")
    @JsonSerialize(using = ToStringSerializer.class)
    private Long roleId;
}
```

**关键点**：
- 继承 `JpaCommonBean` 或 `JpaCommonBean2`
- 使用 `@Getter @Setter`（禁止 @Data）
- 使用 `@Comment` 注解
- Long 类型使用 `@JsonSerialize(using = ToStringSerializer.class)`
- 敏感字段使用 `@JsonIgnore`

#### DAO 层

```java
public interface UserDao extends JpaRepository<User, Long> {
    Optional<User> findByLoginName(String loginName);
}
```

#### Service 层

```java
// Service 接口
public interface UserService extends J2Service<User> {
    Optional<User> findByLoginName(String loginName);
}

// Service 实现
@Service
public class UserServiceImpl extends J2ServiceImpl<UserDao, User, Long>
    implements UserService {

    public UserServiceImpl() {
        super(User.class);
    }

    @Override
    public Optional<User> findByLoginName(String loginName) {
        return findOnly("loginName", loginName);
    }
}
```

**关键点**：
- Service 接口继承 `J2Service<Entity>`
- ServiceImpl 继承 `J2ServiceImpl<DAO, Entity, ID>`（三个泛型）
- 构造函数调用 `super(Entity.class)`
- 可以使用继承的方法：`findOnly()`, `finds()`, `saveOne()` 等

#### Controller 层

```java
@PathRestController("user")
@Tag(name = "用户管理")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("add")
    @Operation(summary = "新增用户")
    public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
        userService.saveCustomer(add);
        return ResultVO.success("新增成功");
    }

    @GetMapping("detail/{id}")
    @Operation(summary = "用户详情")
    public ResultVO<User> detail(@PathVariable Long id) {
        User user = userService.findById(id).orElseThrow();
        return ResultVO.success(user);
    }
}
```

**关键点**：
- 使用 `@PathRestController`（不是 @RestController）
- 返回 `ResultVO<T>` 或 `ResultPageVO<T, JpaPageResult<T>>`
- 使用构造器注入
- 使用 `@Operation`, `@Tag` 注解（Swagger）

#### 请求/响应类

```java
// 请求类（禁止 VO/DTO 后缀）
@Getter
@Setter
@ToString
public class UserAdd {
    @NotBlank(message = "登录名不能为空")
    private String loginName;

    @NotBlank(message = "密码不能为空")
    private String password;
}

// 响应类（仅在需要脱敏时创建）
@Getter
@Setter
@Builder
public class UserInfo {
    private Long id;
    private String loginName;
    // 不包含 password
}
```

---

### 纯 Spring Boot 模式

#### Entity 层

```java
@Entity
@Table(name = "sys_user")
@Data  // 或 @Getter @Setter
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "login_name", nullable = false, unique = true, length = 50)
    private String loginName;

    @Column(name = "password", nullable = false)
    @JsonIgnore
    private String password;

    @Column(name = "role_id")
    private Long roleId;

    @Column(name = "create_time", updatable = false)
    @CreatedDate
    private LocalDateTime createTime;

    @Column(name = "update_time")
    @LastModifiedDate
    private LocalDateTime updateTime;
}
```

**关键点**：
- 不继承基类（或自定义基类）
- 可以使用 `@Data`
- 手动定义所有字段（包括 id、时间戳等）
- 使用标准 JPA 注解

#### Repository 层

```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByLoginName(String loginName);
}
```

#### Service 层

```java
// Service 接口
public interface UserService {
    User save(User user);
    Optional<User> findById(Long id);
    Optional<User> findByLoginName(String loginName);
    List<User> findAll();
    void deleteById(Long id);
}

// Service 实现
@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public User save(User user) {
        return userRepository.save(user);
    }

    @Override
    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    @Override
    public Optional<User> findByLoginName(String loginName) {
        return userRepository.findByLoginName(loginName);
    }

    @Override
    public List<User> findAll() {
        return userRepository.findAll();
    }

    @Override
    public void deleteById(Long id) {
        userRepository.deleteById(id);
    }
}
```

**关键点**：
- 不继承框架基类
- 自定义 Service 接口和方法
- 所有方法需要手动实现

#### Controller 层

```java
@RestController
@RequestMapping("/api/user")
@Tag(name = "用户管理")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping
    @Operation(summary = "新增用户")
    public ResponseEntity<ApiResponse<String>> add(@RequestBody @Valid UserAddDTO dto) {
        userService.save(convertToEntity(dto));
        return ResponseEntity.ok(ApiResponse.success("新增成功"));
    }

    @GetMapping("/{id}")
    @Operation(summary = "用户详情")
    public ResponseEntity<ApiResponse<User>> detail(@PathVariable Long id) {
        User user = userService.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("用户不存在"));
        return ResponseEntity.ok(ApiResponse.success(user));
    }

    private User convertToEntity(UserAddDTO dto) {
        // 转换逻辑
        User user = new User();
        user.setLoginName(dto.getLoginName());
        user.setPassword(dto.getPassword());
        return user;
    }
}
```

**关键点**：
- 使用 `@RestController` + `@RequestMapping`
- 返回 `ResponseEntity<T>` 或自定义返回格式
- 手动处理转换逻辑
- 手动处理异常

#### 请求/响应类

```java
// 请求类（可以使用 DTO 后缀）
@Data
public class UserAddDTO {
    @NotBlank(message = "登录名不能为空")
    private String loginName;

    @NotBlank(message = "密码不能为空")
    private String password;
}

// 响应类（可以使用 VO 后缀）
@Data
public class UserVO {
    private Long id;
    private String loginName;
    // 不包含 password
}
```

---

## 🔄 代码生成决策流程

```
检测到框架类型
    ↓
JDevelops 框架？
├─ 是 → 使用 JDevelops 规范
│       - Entity 继承 JpaCommonBean
│       - Service 继承 J2Service
│       - Controller 使用 @PathRestController
│       - 返回 ResultVO
│       - 禁止 VO/DTO 后缀
│       - 禁止 @Data
│
└─ 否 → 使用 Spring Boot 规范
        - Entity 标准 JPA
        - Service 自定义接口
        - Controller 使用 @RestController
        - 返回 ResponseEntity 或自定义格式
        - 可以使用 DTO/VO 后缀
        - 可以使用 @Data
```

---

## 📌 关键注意事项

### 通用流程（两种模式都适用）

**Entity 字段设计确认**：
- 无论使用哪种模式，都必须在制定开发计划前对每个 Entity 进行字段设计确认
- 详细流程参考：[../workflows/requirement-analysis.md - 步骤 6.5](../workflows/requirement-analysis.md#步骤-65-entity-字段设计确认重要)
- 展示完整字段清单（字段名、类型、长度、约束）
- 支持新增、删除、修改字段
- 迭代直到用户满意

### JDevelops 框架模式

**必须遵守**：
- ✅ 禁止 @Data，使用 @Getter/@Setter
- ✅ 禁止 VO/DTO 后缀，使用意图命名
- ✅ Entity 必须继承 JpaCommonBean
- ✅ Service 必须继承 J2Service
- ✅ Controller 使用 @PathRestController
- ✅ 统一返回 ResultVO

**参考文档**：
- [standards/lombok.md](../standards/lombok.md)
- [standards/naming.md](../standards/naming.md)
- [guides/entity.md](../guides/entity.md)
- [guides/service.md](../guides/service.md)
- [guides/controller.md](../guides/controller.md)

### 纯 Spring Boot 模式

**灵活使用**：
- ✓ 可以使用 @Data
- ✓ 可以使用 DTO/VO 后缀
- ✓ Entity 可以不继承基类
- ✓ Service 自定义接口和方法
- ✓ Controller 使用标准注解
- ✓ 自定义返回格式

**参考**：
- Spring Boot 官方文档
- Spring Data JPA 文档
- 标准 Spring MVC 开发规范

---

## 🎯 检测示例

### 示例 1：JDevelops 项目

**pom.xml**：
```xml
<dependencies>
    <dependency>
        <groupId>cn.tannn.jdevelops</groupId>
        <artifactId>jdevelops-spring-boot-starter</artifactId>
        <version>1.0.3</version>
    </dependency>
    <dependency>
        <groupId>cn.tannn.jdevelops</groupId>
        <artifactId>jdevelops-dals-jpa</artifactId>
        <version>1.0.3</version>
    </dependency>
</dependencies>
```

**检测结果**：
```
检测到项目使用 JDevelops 框架！

【项目信息】
- 框架：JDevelops
- 版本：1.0.3
- 已安装组件：
  - jdevelops-spring-boot-starter
  - jdevelops-dals-jpa

将按照 JDevelops 框架规范生成代码。
```

### 示例 2：纯 Spring Boot 项目

**pom.xml**：
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
    </dependency>
</dependencies>
```

**检测结果**：
```
检测到项目为纯 Spring Boot 项目！

【项目信息】
- 框架：Spring Boot
- Spring Boot 版本：3.2.7
- JPA：Spring Data JPA

将按照标准 Spring Boot 规范生成代码。
```

---

## 📚 相关文档

- SKILL 主文档：[../SKILL.md](../SKILL.md)
- 创建项目工作流：[./create-project.md](./create-project.md)
- 添加模块工作流：[./add-module.md](./add-module.md)
- 需求分析流程：[./requirement-analysis.md](./requirement-analysis.md)
