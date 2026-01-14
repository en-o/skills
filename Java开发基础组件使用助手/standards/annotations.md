# 注解使用规范

## 框架注解

### @PathRestController

**用途**：框架自定义的 Controller 注解，替代 `@RestController` + `@RequestMapping`

**规范**：
- ✅ 使用 `@PathRestController("{path}")`
- ❌ 不使用 `@RestController` + `@RequestMapping`

```java
// ✅ 正确
@PathRestController("user")
@Tag(name = "用户管理")
public class CustomerController {
    // 方法...
}

// ❌ 错误
@RestController
@RequestMapping("/user")
public class CustomerController {
    // 方法...
}
```

---

### @ApiMapping

**用途**：控制接口鉴权

**规范**：
- `checkToken = false`：不需要鉴权（如登录接口）
- `checkToken = true`：需要鉴权（默认）

```java
@PathRestController("auth")
public class AuthController {

    // 不需要鉴权
    @ApiMapping(value = "login", method = RequestMethod.POST, checkToken = false)
    @Operation(summary = "用户登录")
    public ResultVO<String> login(@RequestBody @Valid LoginRequest request) {
        // 登录逻辑
        return ResultVO.success(token);
    }

    // 需要鉴权（默认）
    @GetMapping("info")
    @Operation(summary = "获取当前用户信息")
    public ResultVO<Customer> info() {
        // 获取用户信息
        return ResultVO.success(user);
    }
}
```

---

### @ApiPlatform

**用途**：控制接口平台访问权限

```java
@PathRestController("admin")
public class AdminController {

    @GetMapping("users")
    @Operation(summary = "管理员查询用户列表")
    @ApiPlatform(platform = PlatformConstant.WEB_ADMIN)  // 仅管理员平台可访问
    public ResultVO<List<Customer>> users() {
        return ResultVO.success(users);
    }
}
```

---

## JPA 注解

### Entity 类注解

#### @Entity

**用途**：标记为 JPA 实体类

```java
@Entity
@Table(name = "sys_customer")
public class Customer extends JpaCommonBean {
    // 字段...
}
```

#### @Table

**用途**：指定表名和索引

```java
@Table(
    name = "sys_customer",
    indexes = {
        @Index(name = "idx_login_name", columnList = "loginName", unique = true),
        @Index(name = "idx_phone", columnList = "phone")
    }
)
```

#### @Comment

**用途**：添加表和字段的数据库注释（框架增强）

```java
@Entity
@Table(name = "sys_customer")
@Comment("客户表")
public class Customer extends JpaCommonBean {

    @Column(name = "login_name")
    @Comment("登录名")
    private String loginName;
}
```

---

### 字段注解

#### @Column

**用途**：指定字段的数据库映射属性

**规范**：
- 明确指定 `name`、`nullable`、`length`、`unique` 等属性
- 使用 `columnDefinition` 指定字段类型

```java
// 字符串字段
@Column(name = "login_name", nullable = false, unique = true, length = 50)
private String loginName;

// 数字字段
@Column(name = "status", columnDefinition = "smallint")
private Integer status;

// 大文本字段
@Column(name = "remark", columnDefinition = "text")
private String remark;

// 时间字段
@Column(name = "last_login_time", columnDefinition = "timestamp")
private LocalDateTime lastLoginTime;
```

#### @ColumnDefault

**用途**：指定字段默认值

**注意**：字符串需要加引号

```java
// 数字默认值
@Column(name = "status", columnDefinition = "smallint")
@ColumnDefault("1")
private Integer status;

// 字符串默认值（需要加引号）
@Column(name = "type", columnDefinition = "varchar(20)")
@ColumnDefault("'NORMAL'")
private String type;

// 布尔值默认值
@Column(nullable = false, columnDefinition = "boolean")
@ColumnDefault("false")
private Boolean deleted;
```

#### @Id 和 @GeneratedValue

**用途**：主键标记和生成策略

```java
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
private Long id;

// 或使用框架的自定义生成器
@Id
@GeneratedValue(strategy = GenerationType.AUTO, generator = "uuidCustomGenerator")
@GenericGenerator(name = "uuidCustomGenerator", type = UuidCustomGenerator.class)
@Column(columnDefinition="bigint")
private Long id;
```

---

### 序列化注解

#### @JsonSerialize

**用途**：Long 类型字段防止前端精度丢失

**规范**：所有 Long 类型字段必须添加

```java
@Column(name = "role_id")
@JsonSerialize(using = ToStringSerializer.class)
private Long roleId;

@Column(name = "parent_id")
@JsonSerialize(using = ToStringSerializer.class)
private Long parentId;
```

#### @JsonFormat

**用途**：时间字段格式化

```java
@Column(name = "create_time", columnDefinition = "timestamp")
@JsonFormat(locale = "zh", timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
private LocalDateTime createTime;

@Column(name = "birth_date", columnDefinition = "date")
@JsonFormat(pattern = "yyyy-MM-dd")
private LocalDate birthDate;
```

#### @JsonIgnore

**用途**：永久不序列化字段（如密码）

```java
@Column(name = "password", nullable = false)
@JsonIgnore  // 永不序列化
private String password;

@Column(name = "internal_token")
@JsonIgnore  // 内部字段，不对外暴露
private String internalToken;
```

#### @JsonView

**用途**：按场景控制字段可见性

```java
// 定义视图
public class Views {
    public interface Public {}
    public interface Internal extends Public {}
    public interface Admin extends Internal {}
}

// Entity 中使用
@Getter
@Setter
@Entity
public class Customer extends JpaCommonBean {

    @JsonView(Views.Public.class)
    private Long id;

    @JsonView(Views.Public.class)
    private String loginName;

    @JsonView(Views.Internal.class)
    private String phone;

    @JsonView(Views.Admin.class)
    private String email;
}

// Controller 中使用
@GetMapping("public-info")
@JsonView(Views.Public.class)
public ResultVO<Customer> publicInfo(@RequestParam Long id) {
    return ResultVO.success(customer);
}
```

---

### 关系注解

#### @Enumerated

**用途**：枚举类型字段映射

**规范**：使用 `EnumType.STRING`（不要使用 ORDINAL）

```java
@Column(name = "status")
@Enumerated(EnumType.STRING)
private AccountStatus status;

// 枚举定义
public enum AccountStatus {
    NORMAL, LOCKED, DELETED
}
```

---

## Swagger 注解

### Controller 类注解

#### @Tag

**用途**：标记 API 模块，支持排序

```java
@PathRestController("user")
@Tag(name = "用户管理", extensions = {
    @Extension(properties = {
        @ExtensionProperty(name = "x-order", value = "3", parseValue = true)
    })
})
public class CustomerController {
    // 方法...
}
```

---

### Controller 方法注解

#### @Operation

**用途**：接口说明

**规范**：每个接口方法必须添加

```java
@PostMapping("add")
@Operation(summary = "新增用户")
public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
    return ResultVO.success("新增成功");
}

@GetMapping("detail")
@Operation(summary = "用户详情", description = "根据ID查询用户详细信息")
public ResultVO<Customer> detail(@RequestParam Long id) {
    return ResultVO.success(customer);
}
```

#### @Parameter

**用途**：GET 请求参数说明

```java
@GetMapping("detail")
@Operation(summary = "用户详情")
@Parameter(name = "id", description = "用户ID", required = true)
public ResultVO<Customer> detail(@RequestParam Long id) {
    return ResultVO.success(customer);
}

// 多个参数
@GetMapping("search")
@Operation(summary = "搜索用户")
@Parameter(name = "keyword", description = "搜索关键词", required = true)
@Parameter(name = "status", description = "用户状态", required = false)
public ResultVO<List<Customer>> search(
    @RequestParam String keyword,
    @RequestParam(required = false) Integer status) {
    return ResultVO.success(customers);
}
```

---

### 字段注解

#### @Schema

**用途**：字段说明（Entity、DTO、VO）

```java
@Getter
@Setter
@Entity
public class Customer extends JpaCommonBean {

    @Column(name = "login_name")
    @Schema(description = "登录名", example = "zhangsan")
    private String loginName;

    @Column(name = "status")
    @Schema(description = "状态：1-正常，2-锁定，3-删除")
    private Integer status;
}

// DTO 中使用
@Getter
@Setter
public class UserAdd {

    @NotBlank(message = "登录名不能为空")
    @Schema(description = "登录名", requiredMode = Schema.RequiredMode.REQUIRED)
    private String loginName;

    @NotBlank(message = "密码不能为空")
    @Schema(description = "密码", requiredMode = Schema.RequiredMode.REQUIRED)
    private String password;
}
```

---

## 验证注解

### Bean Validation 注解

```java
@Getter
@Setter
@ToString
public class UserAdd {

    @NotNull(message = "ID不能为空")
    private Long id;

    @NotBlank(message = "登录名不能为空")
    @Size(min = 3, max = 50, message = "登录名长度必须在3-50之间")
    private String loginName;

    @NotBlank(message = "密码不能为空")
    @Size(min = 6, max = 20, message = "密码长度必须在6-20之间")
    private String password;

    @Email(message = "邮箱格式不正确")
    private String email;

    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;

    @Min(value = 1, message = "年龄最小为1")
    @Max(value = 150, message = "年龄最大为150")
    private Integer age;
}
```

### Controller 中使用

```java
@PostMapping("add")
@Operation(summary = "新增用户")
public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
    // @Valid 触发参数验证
    customerService.saveCustomer(add);
    return ResultVO.success("新增成功");
}

// GET 请求参数验证
@GetMapping("detail")
@Operation(summary = "用户详情")
public ResultVO<Customer> detail(
    @RequestParam @NotNull(message = "ID不能为空") Long id) {
    return ResultVO.success(customer);
}
```

---

## 完整示例

### Entity 完整注解

```java
@Getter
@Setter
@Entity
@Table(
    name = "sys_customer",
    indexes = {
        @Index(name = "idx_login_name", columnList = "loginName", unique = true)
    }
)
@Comment("客户表")
@Schema(description = "客户信息")
@DynamicUpdate
@DynamicInsert
public class Customer extends JpaCommonBean {

    @Column(name = "login_name", nullable = false, unique = true, length = 50)
    @Comment("登录名")
    @Schema(description = "登录名", example = "zhangsan")
    @JsonView(Views.Public.class)
    private String loginName;

    @Column(name = "password", nullable = false, length = 100)
    @Comment("密码")
    @Schema(description = "密码")
    @JsonIgnore
    private String password;

    @Column(name = "phone", length = 20)
    @Comment("手机号")
    @Schema(description = "手机号")
    @JsonView(Views.Internal.class)
    private String phone;

    @Column(name = "role_id")
    @Comment("角色ID")
    @Schema(description = "角色ID")
    @JsonSerialize(using = ToStringSerializer.class)
    private Long roleId;

    @Column(name = "status", columnDefinition = "smallint")
    @ColumnDefault("1")
    @Comment("状态：1-正常，2-锁定，3-删除")
    @Schema(description = "状态：1-正常，2-锁定，3-删除")
    private Integer status;

    @Column(name = "last_login_time", columnDefinition = "timestamp")
    @Comment("最后登录时间")
    @Schema(description = "最后登录时间")
    @JsonFormat(locale = "zh", timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime lastLoginTime;
}
```

### Controller 完整注解

```java
@PathRestController("user")
@Tag(name = "用户管理", extensions = {
    @Extension(properties = {
        @ExtensionProperty(name = "x-order", value = "3", parseValue = true)
    })
})
@RequiredArgsConstructor
@Slf4j
@Validated
public class CustomerController {

    private final CustomerService customerService;

    @PostMapping("add")
    @Operation(summary = "新增用户")
    @ApiMapping(checkToken = false)  // 不需要鉴权
    public ResultVO<String> add(@RequestBody @Valid UserAdd add) {
        log.info("新增用户：{}", add);
        customerService.saveCustomer(add);
        return ResultVO.success("新增成功");
    }

    @PostMapping("edit")
    @Operation(summary = "编辑用户")
    public ResultVO<String> edit(@RequestBody @Valid UserEdit edit) {
        log.info("编辑用户：{}", edit);
        customerService.updateCustomer(edit);
        return ResultVO.success("编辑成功");
    }

    @GetMapping("detail")
    @Operation(summary = "用户详情")
    @Parameter(name = "id", description = "用户ID", required = true)
    public ResultVO<Customer> detail(@RequestParam Long id) {
        Customer customer = customerService.findById(id).orElseThrow();
        return ResultVO.success(customer);
    }

    @PostMapping("page")
    @Operation(summary = "分页查询用户")
    @ApiPlatform(platform = PlatformConstant.WEB_ADMIN)
    public ResultPageVO<Customer, JpaPageResult<Customer>> page(
        @RequestBody @Valid UserPage page) {
        Page<Customer> result = customerService.findPage(page, page.getPage());
        JpaPageResult<Customer> pageResult = JpaPageResult.toPage(result, Customer.class);
        return ResultPageVO.success(pageResult, "查询成功");
    }
}
```

---

## 注解优先级和组合

### Entity 必需注解（按优先级）

1. `@Entity`（必需）
2. `@Table`（必需）
3. `@Getter @Setter`（必需）
4. `@Comment`（推荐）
5. `@Schema`（推荐，用于 Swagger）
6. `@DynamicUpdate @DynamicInsert`（可选，优化更新性能）

### Controller 必需注解（按优先级）

1. `@PathRestController`（必需）
2. `@Tag`（必需，用于 Swagger）
3. `@RequiredArgsConstructor`（推荐，用于依赖注入）
4. `@Slf4j`（推荐，用于日志）
5. `@Validated`（可选，用于参数校验）

---

## 参考资源

- 框架源码：https://github.com/en-o/Jdevelops
- 官方文档：https://www.yuque.com/tanning/yg9ipo
- 架构规范：[./architecture.md](./architecture.md)
- Lombok 规范：[./lombok.md](./lombok.md)
